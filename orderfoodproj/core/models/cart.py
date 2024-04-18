from django.db import models 
from .restaurant import Restaurant 
from .dish import Dish
from .user import Customer



class Cart(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='id')
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, null=True, blank=True)
    qty = models.IntegerField(default=1)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    def get_cart_by_user(user):
        return Cart.objects.filter(customer=user)

