from django.shortcuts import render, redirect 
from django.http import HttpResponse, JsonResponse 
from django.contrib.auth.decorators import login_required


from core.models.user import * 
from core.models.cart import Cart

# POST: /add-to-cart/ 
def add_to_cart_api(request):
    # tại trang chủ add bằng json response vào card và cập nhật :)
    return JsonResponse()



@login_required(login_url='/login/')
def cart_detail_view(request):
    # Lấy giỏ hàng của người dùng hiện tại (nếu có)
    user = Customer.objects.get(admin=request.user)
    cart_items = Cart.objects.filter(customer=user)
    
    context = {
        'cart_items': cart_items
    }
    return render(request, 'core/cart.html', context)

# Xử lý hủy đơn hàng
