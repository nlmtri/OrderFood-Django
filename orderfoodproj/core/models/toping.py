from django.db import models 
from .dish import Dish


class Toping(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='id')
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='toping/', null=True, blank=True)
    price = models.IntegerField(default=0)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Toping"
        verbose_name_plural = "Toping"

    def __str__(self):
        return f"{self.id} {self.name} {self.price}"