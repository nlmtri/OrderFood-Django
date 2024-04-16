from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required 
from django.http import HttpResponse, JsonResponse

from core.models.restaurant import Restaurant 
from core.models.dish import Dish 
from core.models.menu import Menu 
from core.models.order import OrderDish 
from core.models.city import City  
from core.models.review import Review 

from django.utils import timezone 
from datetime import datetime, timedelta
from django.db.models import Sum
from django.core.paginator import Paginator
from django.contrib import messages


# GET: /restaurant/burger-king/: có thể thêm slug sau khi hoàn thiện tất cả  
def get_restaurant_view(request, slug):
    try:
        restaurant = Restaurant.objects.get(slug=slug)
    except Restaurant.DoesNotExist:
        messages.info(request, f"Nhà hàng không tồn tại")
        return redirect('index')
    
    dishes = Dish.objects.filter(restaurant=restaurant)
    menu_dict = {}
    for dish in dishes:
        # Nếu dish.menu là null sẽ trả về None, NoneType
        if dish.menu:
            if dish.menu.name not in menu_dict:
                menu_dict[dish.menu.name] = [dish]
            else:
                menu_dict[dish.menu.name].append(dish)
    print(menu_dict)


    # hiển thị ra sản phẩm chính và danh mục các món ăn của nhà hàng cho user
    return render(request, 'core/restaurant-detail.html', {
        'restaurant': restaurant,
        'items': dishes,
        'menu_dict': menu_dict
    }, status=200)


# GET: /restaurant-admin/ 
@login_required(login_url='/login/')
def get_restaurant_admin_view(request):
    if request.user.user_type == '2':
        if request.user.provider.restaurant.is_active:
            restaurant = request.user.provider.restaurant
            total_order, orders = OrderDish.get_total_order_of_restaurant_every_day(restaurant)
            total_completed_order, total_price = OrderDish.get_total_order_of_restaurant_completed_every_day(restaurant=restaurant)
            total_cancel_order = OrderDish.get_total_order_cancel(restaurant)

            titles = ["STT", "Thời gian", "Trạng thái", "Giá"]
            items_per_page = 8
            p = Paginator(orders, items_per_page)
            page = request.GET.get('page')
            items = p.get_page(page)
            current = items.number
            start = max(current - 2, 1)
            end = min(current + 2, items.paginator.num_pages)
            page_range = range(start, end)
            start_number = (current - 1) * items_per_page

            return render(request, 'restaurant_admin/index.html', {
                'total_order': total_order,
                'total_completed_order': total_completed_order,
                'total_cancel_order': total_cancel_order,
                'total_price': total_price,
                'titles': titles,
                'items': items, 
                'start': start, 
                'end': end, 
                'page_range': page_range,
                'start_number': start_number,
                'restaurant': restaurant
            }, status=200)
        else:
            return HttpResponse("<h1>Sau khi được duyệt nhà hàng có thể truy cập vào trang quản lý</h1><h3>Quá trình chờ duyệt trong 24h</h3>")
    else:
        return render(request, 'handle_error/403.html')

    
# GET: /restaurant-admin/7-day-statistic/
@login_required(login_url='/login/')
def get_7_day_statistic_api(request):
    if request.user.user_type == '2':
        if request.user.provider.restaurant.is_active:
            restaurant = request.user.provider.restaurant
            days = 7
            end_date =  timezone.now().date() - timedelta(days=1) 
            start_date = end_date - timedelta(days=days-1)
            fdays = []
            revenues = []
            for single_date in (start_date + timedelta(n) for n in range(days)):
                day_start = datetime(single_date.year, single_date.month, single_date.day, 0, 0, 0, tzinfo=timezone.get_current_timezone())
                day_end = datetime(single_date.year, single_date.month, single_date.day, 23, 59, 59, tzinfo=timezone.get_current_timezone())
                total_revenue = OrderDish.objects.filter(
                    restaurant=restaurant,
                    created_at__range=(day_start, day_end),
                    status="Hoàn thành"
                ).aggregate(total=Sum('price'))['total'] or 0 
                # aggregation: tổng hợp: tóm tắt tổng hợp các đối tượng
                revenues.append(total_revenue)
                fdays.append(f"{single_date.day}-{single_date.month}-{single_date.year}")
            # print(revenues)
            # print(fdays)
            return JsonResponse({
                'success': True,
                'message': "Lấy dữ liệu thống kê thành công!",
                'bundle': {
                    'revenues': revenues,
                    'days': fdays,
                },
                'status': 200
            }, status=200)
        else:
            return JsonResponse({
                'success': False,
                'message': 'Chờ duyệt trong 24h',
                'bundle': {},
                'status': 403
            }, status=403)
    else:
        return JsonResponse({
            'success': False,
            'message': "Permission not allowed",
            'bundle': {},
            'status': 403
        }, status=403) 
    

# GET: /restaurant-admin/profile/xoi-chu-ngong/
@login_required(login_url='/login/')
def get_edit_profile_restaurant_view(request, slug):
    if request.user.user_type == '2':
        if request.user.provider.restaurant.is_active:
            restaurant = request.user.provider.restaurant
            cities = City.objects.all().order_by('name')
            return render(request, 'restaurant_admin/profile.html', {
                'restaurant': restaurant,
                'cities': cities
            }, status=200)
        else:
            return HttpResponse("<h1>Sau khi được duyệt nhà hàng có thể truy cập vào trang quản lý</h1><h3>Quá trình chờ duyệt trong 24h</h3>")
    else:
        return render(request, 'handle_error/403.html') 


# POST: /restaurant-admin/profile/save/xoi-chu-ngong/ 
@login_required(login_url='/login/')
def post_save_profile_restaurant_admin_view(request, slug):
    if request.user.user_type == '2':
        if request.user.provider.restaurant.is_active:
            if request.method == 'POST':
                restaurant = request.user.provider.restaurant
                restaurant.name = request.POST.get('rest-name')
                restaurant.address = request.POST.get('address')
                restaurant.phone_number = request.POST.get('phone-number')
                
                try:
                    city = City.objects.get(pk=request.POST.get('city'))
                except City.DoesNotExist:
                    messages.info(request, "Thành phố không tồn tại")
                    return redirect('restaurant-profile-admin-view', request.user.provider.restaurant.slug)

                restaurant.city = city 

                if request.FILES.get('banner') is not None:
                    restaurant.banner = request.FILES.get('banner')
                
                if request.FILES.get('logo') is not None:
                    restaurant.logo = request.FILES.get('logo')
                restaurant.save()
                messages.info(request, "Cập nhật thông tin nhà hàng thành công!")
                return redirect('restaurant-profile-admin-view', request.user.provider.restaurant.slug)
            else:
                return redirect('restaurant-profile-admin-view', request.user.provider.restaurant.slug)
        else:
            return HttpResponse("<h1>Sau khi được duyệt nhà hàng có thể truy cập vào trang quản lý</h1><h3>Quá trình chờ duyệt trong 24h</h3>")
    else:
        return render(request, 'handle_error/403.html') 


# GET: /restaurant-admin/dish/
@login_required(login_url='/login/')
def get_dish_admin_view(request):
    if request.user.user_type == '2':
        if request.user.provider.restaurant.is_active:
            restaurant = request.user.provider.restaurant
            dishes = Dish.objects.filter(restaurant=restaurant).order_by('-id')

            titles = ["STT", "Tên món ăn", "Thực đơn", "Ảnh", "Giá", "Thao tác"]

            items_per_page = 3
            p = Paginator(dishes, items_per_page)
            page = request.GET.get('page')
            items = p.get_page(page)
            current = items.number
            start = max(current - 2, 1)
            end = min(current + 2, items.paginator.num_pages)
            page_range = range(start, end)
            start_number = (current - 1) * items_per_page

            return render(request, 'restaurant_admin/dish.html', {
                'titles': titles,
                'restaurant': restaurant,
                'items': items, 
                'start': start, 
                'end': end, 
                'page_range': page_range,
                'start_number': start_number,
                'restaurant': restaurant
            }, status=200)
        else:
            return HttpResponse("<h1>Sau khi được duyệt nhà hàng có thể truy cập vào trang quản lý</h1><h3>Quá trình chờ duyệt trong 24h</h3>")
    else:
        return render(request, 'handle_error/403.html') 


# GET: /restaurant-admin/order/
@login_required(login_url='/login/')
def get_order_admin_view(request):
    if request.user.user_type == '2':
        if request.user.provider.restaurant.is_active:
            restaurant = request.user.provider.restaurant
            titles = ["STT", "Món ăn", "Số lượng", "Tổng tiền", "Thời gian", "Trạng thái", "Thao tác"]
            orders = OrderDish.objects.filter(restaurant=restaurant).order_by('-created_at')

            items_per_page = 7
            p = Paginator(orders, items_per_page)
            page = request.GET.get('page')
            items = p.get_page(page)
            current = items.number
            start = max(current - 2, 1)
            end = min(current + 2, items.paginator.num_pages)
            page_range = range(start, end)
            start_number = (current - 1) * items_per_page

            return render(request, 'restaurant_admin/order.html', {
                'titles': titles,
                'items': items, 
                'start': start, 
                'end': end, 
                'page_range': page_range,
                'start_number': start_number,
                'restaurant': restaurant
                
            }, status=200)
        else:
            return HttpResponse("<h1>Sau khi được duyệt nhà hàng có thể truy cập vào trang quản lý</h1><h3>Quá trình chờ duyệt trong 24h</h3>")
    else:
        return render(request, 'handle_error/403.html') 


# GET: /restaurant-admin/review/
@login_required(login_url='/login/')
def get_review_admin_view(request):
    if request.user.user_type == '2':
        if request.user.provider.restaurant.is_active:
            restaurant = request.user.provider.restaurant
            dishes = Dish.get_dishes_by_restaurant(restaurant)

            titles = ["STT", "Tên tài khoản", "Đánh giá", "Món ăn", "Trạng thái"]

            items_per_page = 6
            p = Paginator(dishes, items_per_page)
            page = request.GET.get('page')
            items = p.get_page(page)
            current = items.number
            start = max(current - 2, 1)
            end = min(current + 2, items.paginator.num_pages)
            page_range = range(start, end)
            start_number = (current - 1) * items_per_page

            return render(request, 'restaurant_admin/review.html', {
                'titles': titles,
                'items': items, 
                'start': start, 
                'end': end, 
                'page_range': page_range,
                'start_number': start_number,
                'restaurant': restaurant
            }, status=200)
        else:
            return HttpResponse("<h1>Sau khi được duyệt nhà hàng có thể truy cập vào trang quản lý</h1><h3>Quá trình chờ duyệt trong 24h</h3>")
    else:
        return render(request, 'handle_error/403.html')


# GET: /restaurant-admin/report/
@login_required(login_url='/login/')
def get_report_admin_view(request):
    if request.user.user_type == '2':
        if request.user.provider.restaurant.is_active:
            restaurant = request.user.provider.restaurant
            cities = City.objects.all().order_by('name')
            return render(request, 'restaurant_admin/profile.html', {
                'restaurant': restaurant,
                'cities': cities
            }, status=200)
        else:
            return HttpResponse("<h1>Sau khi được duyệt nhà hàng có thể truy cập vào trang quản lý</h1><h3>Quá trình chờ duyệt trong 24h</h3>")
    else:
        return render(request, 'handle_error/403.html')
    return render(request, 'restaurant_admin/report.html', {})


# GET: /restaurant-admin/revenues/
@login_required(login_url='/login/')
def get_revenues_admin_view(request):
    if request.user.user_type == '2':
        if request.user.provider.restaurant.is_active:
            restaurant = request.user.provider.restaurant
            cities = City.objects.all().order_by('name')
            return render(request, 'restaurant_admin/profile.html', {
                'restaurant': restaurant,
                'cities': cities
            }, status=200)
        else:
            return HttpResponse("<h1>Sau khi được duyệt nhà hàng có thể truy cập vào trang quản lý</h1><h3>Quá trình chờ duyệt trong 24h</h3>")
    else:
        return render(request, 'handle_error/403.html')
    return render(request, 'restaurant_admin/revenues.html', {})



