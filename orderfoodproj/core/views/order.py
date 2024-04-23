from django.shortcuts import render, redirect 
from  django.contrib.auth.decorators import login_required 
from django.contrib import messages 
from django.http import HttpResponse, JsonResponse

from core.models.order import * 
from core.models.user import * 
from core.models.cart import *
from core.models.review import *
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
def order_history_view(request):
    user = Customer.objects.get(admin=request.user)
    orders = Order.objects.filter(customer=user).prefetch_related('orderdish_set')
    detailed_orders = []

    if request.method == 'POST':
        dish_id = request.POST.get('dish_id')
        review_text = request.POST.get('review')
        rating = int(request.POST.get('rating', 0))
        dish = Dish.objects.get(pk=dish_id)
        
        # Check if the review already exists
        review, created = Review.objects.get_or_create(
            user=user,
            dish=dish,
            defaults={'review': review_text, 'rating': rating}
        )
        
        if not created:  # If the review exists, update it
            review.review = review_text
            review.rating = rating
            review.save()
            return redirect('order_history')  # Redirect to avoid double posting if the user refreshes the page

    for order in orders:
        dishes = order.orderdish_set.all()
        detailed_dishes = []
        for dish in dishes:
            try:
                review = Review.objects.get(user=user, dish=dish.dish)
                dish.existing_review = review
            except Review.DoesNotExist:
                dish.existing_review = None

            detailed_dishes.append({
                'id': dish.dish.id,
                'name': dish.dish.name,
                'quantity': dish.quantity,
                'price_per_item': dish.dish.price,
                'total_price_per_dish': dish.quantity * dish.dish.price,
                'existing_review': dish.existing_review,
            })
        detailed_orders.append({
            'id': order.id,
            'delivery_address': order.delivery_address,
            'phone_number': order.phone_number,
            'created_at': order.created_at,
            'total_price': order.total_price,
            'dishes': detailed_dishes,
        })

    return render(request, 'core/orders.html', {'orders': detailed_orders})

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

