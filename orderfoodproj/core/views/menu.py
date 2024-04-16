from django.shortcuts import render, redirect 
from django.core.paginator import Paginator 
from django.contrib import messages 

from core.models.menu import * 
from core.models.dish import * 


# GET: /menu/fast-food/
def get_menu_detail_view(request, slug):
    categories = Menu.get_menu_by_quantity()
    try:
        menu = Menu.objects.get(slug=slug)
    except Menu.DoesNotExist:
        messages.info(request, f"Không tìm thấy menu với slug = {slug}")
        return redirect('index')
    dishes = Dish.objects.filter(menu=menu).order_by('name')
    items_per_page = 10 
    p = Paginator(dishes, items_per_page)
    page = request.GET.get('page')
    items = p.get_page(page)

    current = items.number 
    start = max(current - 2, 1)
    end = min(current + 2, items.paginator.num_pages)
    page_range = range(start, end)
    start_number = (current - 1) * items_per_page

    return render(request, 'core/menu-detail.html', {
        'categories': categories,
        'items': items, 
        'start': start,
        'end': end,
        'page_range': page_range,
        'start_number': start_number,
        'menu': menu
    }, status=200)
