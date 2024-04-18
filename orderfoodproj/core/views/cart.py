from django.shortcuts import render, redirect 
from django.http import HttpResponse, JsonResponse 
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from collections import defaultdict


from core.models.user import * 
from core.models.cart import Cart
from core.models.cart import Dish



@login_required(login_url='/login/')
@require_POST  # Ensures that this view can only handle POST requests
def add_to_cart(request):
    dish_id = request.POST.get('dish_id')
    qty = request.POST.get('qty', 1)  # Default to 1 if qty not provided
    note = request.POST.get('note', '')  # Default to empty string if no note provided
    dish = Dish.objects.get(id=dish_id)
    customer = Customer.objects.get(admin=request.user)  # Adjusted to directly access the customer relation

    cart_item, created = Cart.objects.get_or_create(
        dish=dish,
        customer=customer,
        defaults={'qty': qty, 'note': note}
    )
    if not created:
        cart_item.qty += int(qty)
        cart_item.note = note  # Update the note
        cart_item.save()

    return redirect('cart-detail-view')

@login_required(login_url='/login/')
def cart_detail_view(request):
    user = Customer.objects.get(admin=request.user)
    cart_items = Cart.objects.filter(customer=user).select_related('dish__restaurant')
    items_by_restaurant = defaultdict(list)

    for item in cart_items:
        items_by_restaurant[item.dish.restaurant.name].append(item)

    context = {
        'items_by_restaurant': dict(items_by_restaurant),
        'total_qty': sum(item.qty for item in cart_items),
        'total_price': sum(item.qty * item.dish.price for item in cart_items)
    }
    return render(request, 'core/cart.html', context)

@require_POST
def update_cart(request, item_id):
    cart_item = Cart.objects.get(id=item_id)
    qty = request.POST.get('qty', 1)
    note = request.POST.get('note', '')  # Get the note from POST data, defaulting to empty string

    if qty:
        cart_item.qty = int(qty)
        cart_item.note = note  # Update the note field
        cart_item.save()
    return redirect('cart-detail-view')

def remove_from_cart(request, item_id):
    cart_item = Cart.objects.get(id=item_id)
    cart_item.delete()
    return redirect('cart-detail-view')

# Xử lý hủy đơn hàng
