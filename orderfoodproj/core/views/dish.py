from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required 
from django.http import JsonResponse 
from django.contrib import messages 

from core.models.dish import Dish
from core.models.toping import Toping 
from core.models.menu import Menu


# GET: /dishes/5/
def get_dish_data_api(request, pk):
    try:
        dish = Dish.objects.get(pk=pk)
    except Dish.DoesNotExist:
        return JsonResponse({
            'message': 'Món ăn không tồn tại',
            'success': False,
            'bundle': {},
            'status': 404
        }, status=404)
    topings = Toping.objects.filter(dish=dish)
    data = []
    for t in topings:
        obj = {
            'name': obj.name,
            'price': obj.price
        }
        data.append(obj)
    return JsonResponse({
        'message': 'Lấy dữ liệu món ăn thành công!',
        'success': True,
        'bundle': {
            'dish': {
                'name': dish.name,
                'price': dish.price,
                'url': dish.image.url
            },
            'topings': data
        },
        'status': 200
    }, status=200)


# GET: /restaurant-admin/add-dish/
@login_required(login_url='/login/')
def get_add_dish_admin_view(request):
    if request.user.user_type == '2':
        if request.user.provider.restaurant.is_active:
            menus = Menu.objects.all().order_by('name')
            return render(request, 'restaurant_admin/add-dish.html', {
                'menus': menus,
            }, status=200) 
        else:
            return HttpResponse("<h1>Sau khi được duyệt nhà hàng có thể truy cập vào trang quản lý</h1><h3>Quá trình chờ duyệt trong 24h</h3>")
    else:
        return render(request, 'handle_error/403.html')


# POST: /restaurant-admin/add-dish/save/
@login_required(login_url='/login/')
def post_add_dish_admin_view(request):
    if request.user.user_type == '2':
        if request.user.provider.restaurant.is_active:
            if request.method == 'POST':
                try:
                    menu = Menu.objects.get(pk=request.POST.get('menu'))
                except Menu.DoesNotExist:
                    messages.info(request, 'Menu không tồn tại!')
                    return redirect('add-dish-admin-view')
                if request.FILES.get('dish-image') is not None:
                    dish = Dish(
                        name=request.POST.get('dish-name'),
                        image=request.FILES.get('dish-image'),
                        price=request.POST.get('price'),
                        restaurant=request.user.provider.restaurant,
                        menu=menu,
                        type=request.POST.get('dish-type'),
                        description=request.POST.get('description'),
                        distance = request.POST.get('distance')
                    )
                    dish.save()
                    messages.info(request, "Thêm món ăn thành công!")
                    return redirect('dish-admin-view')
                else:
                    messages.info(request, "Ảnh món ăn là bắt buộc")
                    return redirect('add-dish-admin-view')
            else:
                return redirect('add-dish-admin-view') 
        else:
            return HttpResponse("<h1>Sau khi được duyệt nhà hàng có thể truy cập vào trang quản lý</h1><h3>Quá trình chờ duyệt trong 24h</h3>")
    else:
        return render(request, 'handle_error/403.html') 


# GET: /restaurant-admin/edit-dish/5/
@login_required(login_url='/login/')
def get_edit_dish_admin_view(request, pk):
    if request.user.user_type == '2':
        if request.user.provider.restaurant.is_active:
            try:
                dish = Dish.objects.get(pk=pk)
            except Dish.DoesNotExist:
                messages.info(request, "Không tìm thấy thông tin món ăn!")
                return redirect('dish-admin-view')
            menus = Menu.objects.all().order_by('name')
            return render(request, 'restaurant_admin/edit-dish.html', {
                'dish': dish,
                'menus': menus
            }, status=200) 
        else:
            return HttpResponse("<h1>Sau khi được duyệt nhà hàng có thể truy cập vào trang quản lý</h1><h3>Quá trình chờ duyệt trong 24h</h3>")
    else:
        return render(request, 'handle_error/403.html') 


# POST: /restaurant-admin/edit-dish/save/5/
@login_required(login_url='/login/')
def post_edit_dish_admin_view(request, pk):
    if request.user.user_type == '2':
        if request.user.provider.restaurant.is_active:
            if request.method == 'POST':

                try:
                    menu = Menu.objects.get(pk=request.POST.get('menu'))
                except Menu.DoesNotExist:
                    messages.info(request, 'Menu không tồn tại!')
                    return redirect('dish-admin-view')

                try:
                    dish = Dish.objects.get(pk=pk)
                except Dish.DoesNotExist:
                    messages.info(request, "Không tìm thấy thông tin món ăn!")
                    return redirect('dish-admin-view')

                if request.FILES.get('dish-image') is not None:
                    dish.image = request.FILES.get('dish-image')
                dish.name = request.POST.get('dish-name')
                dish.price = request.POST.get('price')
                dish.menu = menu 
                dish.type = request.POST.get('dish-type')
                dish.description = request.POST.get('description')
                dish.distance = request.POST.get('distance')
                dish.save()

                messages.info(request, "Cập nhật món ăn thành công!")
                return redirect('dish-admin-view')

            else:
                return redirect('edit-dish-admin-view', pk) 
        else:
            return HttpResponse("<h1>Sau khi được duyệt nhà hàng có thể truy cập vào trang quản lý</h1><h3>Quá trình chờ duyệt trong 24h</h3>")
    else:
        return render(request, 'handle_error/403.html') 


# POST: /restaurant-admin/delete/dish/5/
@login_required(login_url='/login/')
def post_delete_dish_admin_view(request, pk):
    if request.user.user_type == '2':
        if request.user.provider.restaurant.is_active:
            try:
                dish = Dish.objects.get(pk=pk)
            except Dish.DoesNotExist:
                messages.info(request, "Không tìm thấy món ăn!")
                return redirect('dish-admin-view')  
            dish.delete()
            messages.info(request, "Xóa món ăn thành công!")
            return redirect('dish-admin-view')
        else:
            return HttpResponse("<h1>Sau khi được duyệt nhà hàng có thể truy cập vào trang quản lý</h1><h3>Quá trình chờ duyệt trong 24h</h3>")
    else:
        return render(request, 'handle_error/403.html') 
