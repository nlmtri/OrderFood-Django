from django.db import models
from django.db.models import Q


class City(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='id')
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_all_cities():
        '''Trả về tất cả City có trong database'''
        return City.objects.all()

    @staticmethod
    def get_city_by_name(name):
        # unaccent__icontains: tìm kiếm không dấu
        return City.objects.filter(Q(name__icontains=name) | Q(name__unaccent__icontains=name))

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "City"
    
    def __str__(self):
        return f"ID: {self.id} - {self.name}"
