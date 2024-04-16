from django.shortcuts import render, redirect 
from django.core.paginator import Paginator
from django.db.models import Q

import random

from core.models.dish import * 
from core.models.menu import * 


# GET: 127.0.0.1:8000
def index(request):
    query = request.GET.get('q')

    feature_list = list(Dish.objects.filter(featured=True))
    random.shuffle(feature_list)
    feature_list = feature_list[:4]

    categories = Menu.get_menu_by_quantity()
    dishes = Dish.objects.all().order_by('name')

    if query is not None:
        dishes = Dish.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) | 
            Q(type__icontains=query) | 
            Q(menu__name__icontains=query) | 
            Q(restaurant__name__icontains=query) | 
            Q(restaurant__address__icontains=query)
        ).order_by('name')
    else:
        query = ''

    items_per_page = 10
    p = Paginator(dishes, items_per_page)
    page = request.GET.get('page')
    items = p.get_page(page)

    current = items.number 
    start = max(current - 2, 1)
    end = min(current + 2, items.paginator.num_pages)
    page_range = range(start, end)
    start_number = (current - 1) * items_per_page

    return render(request, 'core/index.html', {
        'feature_list': feature_list,
        'categories': categories,
        'items': items, 
        'start': start,
        'end': end,
        'page_range': page_range,
        'start_number': start_number,
        'query': query
    }, status=200)
