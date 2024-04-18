from django.shortcuts import render, redirect 
from django.http import HttpResponse, JsonResponse 
from django.contrib.auth.decorators import login_required


from core.models.user import * 
from core.models.cart import Cart
from core.models.cart import Dish

# GET: /add-to-cart/<dish_id>/<qty>/
def add_to_cart(request, dish_id, qty):
    dish = Dish.objects.get(id=dish_id)
    customer = Customer.objects.get(admin=request.user)  # Assuming the Customer model is linked to User
    cart_item, created = Cart.objects.get_or_create(
        dish=dish,
        customer=customer,
        defaults={'qty': qty}
    )
    if not created:
        cart_item.qty += int(qty)
        cart_item.save()
    
    # Redirect to a new URL, e.g., cart page or home page
    return redirect('cart-detail-view')


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
