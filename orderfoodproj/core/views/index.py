from django.shortcuts import render, redirect 
from django.core.paginator import Paginator
from django.db.models import Q, Avg

import random

from core.models.dish import * 
from core.models.menu import * 


# GET: 127.0.0.1:8000
def index(request):
    query = request.GET.get('q')

    # Get a list of featured dishes (randomly selected)
    feature_list = list(Dish.objects.all())
    random.shuffle(feature_list)
    feature_list = feature_list[:4]

    # Get all menu categories
    categories = Menu.get_all_menu()

    # Get all dishes with average ratings, ordered by name
    dishes = Dish.objects.annotate(avg_rating=Avg('review__rating')).order_by('name')

    # Filter dishes based on search query
    if query is not None:
        dishes = dishes.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) | 
            Q(type__icontains=query) | 
            Q(menu__name__icontains=query) | 
            Q(restaurant__name__icontains=query) | 
            Q(restaurant__address__icontains=query)
        ).order_by('name')
    else:
        query = ''

    # Paginate the dishes
    items_per_page = 18
    paginator = Paginator(dishes, items_per_page)
    page_number = request.GET.get('page')
    items = paginator.get_page(page_number)

    # Determine the pagination range
    current_page_number = items.number
    start_page = max(current_page_number - 2, 1)
    end_page = min(current_page_number + 2, paginator.num_pages)
    page_range = range(start_page, end_page)
    start_number = (current_page_number - 1) * items_per_page

    return render(request, 'core/index.html', {
        'feature_list': feature_list,
        'categories': categories,
        'items': items,
        'start_page': start_page,
        'end_page': end_page,
        'page_range': page_range,
        'start_number': start_number,
        'query': query
    })