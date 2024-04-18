from django.shortcuts import render, redirect 
from  django.contrib.auth.decorators import login_required 
from django.contrib import messages 
from django.http import HttpResponse, JsonResponse

from core.models.order import * 
from core.models.user import * 
from core.models.cart import *
from collections import defaultdict

def order_view(request):
    pass 


@login_required(login_url='/login/')
def place_order_view(request):
    user = Customer.objects.get(admin=request.user)
    cart_items = Cart.objects.filter(customer=user).select_related('dish', 'dish__restaurant')
    items_by_restaurant = defaultdict(list)
    
    for item in cart_items:
        items_by_restaurant[item.dish.restaurant.name].append(item)
    
    total_price = sum(item.qty * item.dish.price for item in cart_items)
    
    context = {
        'items_by_restaurant': dict(items_by_restaurant),
        'total_price': total_price,
    }
    return render(request, 'core/place-order.html', context)

@login_required(login_url='/login/')
def submit_order_view(request):
    if request.method == 'POST':
        customer = Customer.objects.get(admin=request.user)
        address = request.POST['address']
        phone_number = request.POST['phone']

        # Grouping cart items by restaurant
        cart_items = Cart.objects.filter(customer=customer).select_related('dish', 'dish__restaurant')
        items_by_restaurant = defaultdict(list)
        for item in cart_items:
            items_by_restaurant[item.dish.restaurant].append(item)

        # Create an order for each restaurant
        for restaurant, items in items_by_restaurant.items():
            total_price = sum(item.qty * item.dish.price for item in items)
            order = Order.objects.create(
                customer=customer,
                total_price=total_price,
                restaurant=restaurant,
                status='Đang chờ xử lý',  # Default status
                delivery_address=address,
                phone_number=phone_number,
                created_at=timezone.now()
            )

            # Create OrderDish for each item in the order
            for item in items:
                OrderDish.objects.create(
                    order=order,
                    dish=item.dish,
                    quantity=item.qty,
                    note=item.note,
                )

            # Optionally clear the cart items
            # item.delete()  # Uncomment this line if you want to clear the cart after order

        return redirect('order_success')  # Redirect to an order success page or similar

    return redirect('place_order')  # Redirect back if not a POST request or fail

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
                    order = Order.objects.get(pk=pk)
                except Order.DoesNotExist:
                    messages.info(request, "Đơn đặt món không tồn tại!")
                    return redirect('order-admin-view')
                order.status = request.POST.get('order-status')
                order.save()
                messages.info(request, "Cập nhật tình trạng đơn thành công!!")
                return redirect('order-admin-view')

            else:
                return redirect('order-admin-view')
        else:
            return HttpResponse("<h1>Sau khi được duyệt nhà hàng có thể truy cập vào trang quản lý</h1><h3>Quá trình chờ duyệt trong 24h</h3>")
    else:
        return render(request, 'handle_error/403.html') 

    
# GET: /restaurant-admin/order/5/
@login_required
def get_detail_order_admin_api(request, pk):
    if request.user.user_type == '2':
        if request.user.provider.restaurant.is_active:
            try:
                order = Order.objects.get(pk=pk, restaurant=request.user.provider.restaurant)
            except Order.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'Không tìm thấy đơn đặt hàng!',
                    'bundle': {},
                    'status': 404,
                }, status=404)

            # Get related OrderDish items
            order_dishes = OrderDish.objects.filter(order=order)
            dishes_details = []
            for order_dish in order_dishes:
                dishes_details.append({
                    'dish': order_dish.dish.name,
                    'image_url': order_dish.dish.image.url,
                    'dish_description': order_dish.dish.description,
                    'price': order_dish.dish.price,
                    'quantity': order_dish.quantity,
                    'note': order_dish.note,
                })

            return JsonResponse({
                'success': True, 
                'message': "Lấy dữ liệu thành công!!",
                'bundle': {
                    "user_order": order.customer.admin.username,
                    'address': order.delivery_address,
                    'phone': order.phone_number,
                    'dishes': dishes_details,
                    'time': order.created_at.strftime("%Y-%m-%d %H:%M:%S")
                }, 
                'status': 200
            }, status=200)

        else:
            return HttpResponse("<h1>Sau khi được duyệt nhà hàng có thể truy cập vào trang quản lý</h1><h3>Quá trình chờ duyệt trong 24h</h3>")
    else:
        return render(request, 'handle_error/403.html')