from django.shortcuts import render, redirect 
from django.http import HttpResponse, JsonResponse 
from django.contrib.auth.decorators import login_required

# POST: /add-to-cart/ 
def add_to_cart_api(request):
    # tại trang chủ add bằng json response vào card và cập nhật :)
    return JsonResponse()


# @login_required(login_url='/login/')
def cart_detail_view(request):
    # View, cart, add not, increment or decrement quantity 
    return render(request, 'core/cart.html', {})


# Xử lý hủy đơn hàng
