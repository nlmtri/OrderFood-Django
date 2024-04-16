from django.contrib import admin
from .models.user import * 
from .models.city import City 
from .models.dish import Dish 
from .models.menu import Menu 
from .models.order import Order, OrderDish
from .models.restaurant import Restaurant 
from .models.review import Review


# username: admin
# email: admin@gmail.com 
# password: @Admin1019

from django.contrib.auth.admin import UserAdmin 


class UserModel(UserAdmin):
    list_display = ('username', 'email')
    search_fields = ('username', 'email')


admin.site.register(CustomUser, UserModel)
admin.site.register(City)
admin.site.register(Dish)
admin.site.register(Menu)
admin.site.register(Order)
admin.site.register(OrderDish)
admin.site.register(Restaurant)
admin.site.register(Review)

