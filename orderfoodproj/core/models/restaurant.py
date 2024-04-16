from django.db import models 
from django.db.models import Q
from .city import City


class Restaurant(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='id')
    name = models.CharField(max_length=255) 
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    logo = models.ImageField(upload_to='rest-logo/', default='default/logo.png')
    banner = models.ImageField(upload_to='banners/', default='default/banner.png')
    created_at = models.DateTimeField(auto_now_add=True) 

    city = models.ForeignKey(City, on_delete=models.DO_NOTHING, default=1)
    slug = models.SlugField(null=True, blank=True)

    is_active = models.BooleanField(default=False) # trạng thái nhà hàng được duyệt hay chưa?

    @staticmethod
    def get_all_restaurants():
        return Restaurant.objects.all()

    @staticmethod
    def get_restaurant_by_city(city_name):
        return Restaurant.objects.filter(Q(city__name__icontains=city_name) | Q(city__name__unaccent__icontains=city_name))

    class Meta:
        verbose_name = 'Restaurant'
        verbose_name_plural = 'Restaurant'

    def __str__(self):
        return f"ID: {self.id} - Name: {self.name} - City:{self.city.name}"    
