from django.shortcuts import render, redirect 
from  django.contrib.auth.decorators import login_required 
from django.contrib import messages 
from django.http import HttpResponse, JsonResponse

from core.models.order import OrderDish 


def order_view(request):
    pass 


def checkout_view(request):
    pass 


def tracking_order_view(request):
    pass 
    # Theo dõi tình trạng đơn hàng 


def export_bill_view(request):
    pass 
    # export pdf cho phép in ra


# POST: /restaurant-admin/update-order/<pk>
@login_required(login_url='/login/')
def post_update_order_admin_view(request, pk):
    if request.user.user_type == '2':
        if request.user.provider.restaurant.is_active:
            if request.method == 'POST':

                try:
                    order_dish = OrderDish.objects.get(pk=pk)
                except OrderDish.DoesNotExist:
                    messages.info(request, "Đơn đặt món không tồn tại!")
                    return redirect('order-admin-view')
                order_dish.status = request.POST.get('order-status')
                order_dish.save()
                messages.info(request, "Cập nhật tình trạng đơn thành công!!")
                return redirect('order-admin-view')

            else:
                return redirect('order-admin-view')
        else:
            return HttpResponse("<h1>Sau khi được duyệt nhà hàng có thể truy cập vào trang quản lý</h1><h3>Quá trình chờ duyệt trong 24h</h3>")
    else:
        return render(request, 'handle_error/403.html') 

    
# GET: /restaurant-admin/order/5/
def get_detail_order_admin_api(request, pk):
    if request.user.user_type == '2':
        if request.user.provider.restaurant.is_active:
            try:
                order_dish = OrderDish.objects.get(pk=pk)
            except OrderDish.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'Không tìm thấy đơn đặt hàng!',
                    'bundle': {},
                    'status': 404,
                }, status=404)

            return JsonResponse({
                'success': True, 
                'message': "Lấy dữ liệu thành công!!",
                'bundle': {
                    "user_order": order_dish.order.customer.admin.username,
                    'address': order_dish.delivery_address,
                    'phone': order_dish.phone_number,
                    'dish': order_dish.dish.name,
                    'image_url': order_dish.dish.image.url,
                    'dish_description': order_dish.dish.description,
                    'price': order_dish.price,
                    'quantity': order_dish.quantity, 
                    'note': order_dish.note,
                    'time': order_dish.created_at,
                }, 
                'status': 200
            }, status=200)

        else:
            return JsonResponse({
                'success': False,
                'message': 'Vui lòng chờ duyệt trong 24h',
                'bundle': {},
                'status': 403,
            }, status=403)
    else:
        return JsonResponse({
            'success': False,
            'message': 'Permission Error',
            'bundle': {},
            'status': 403
        }, status=403)
