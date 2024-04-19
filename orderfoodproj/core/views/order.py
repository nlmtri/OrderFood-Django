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

