from django.db import models 
from .dish import Dish 
from .user import Customer 


class Review(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='id')
    user = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, null=True, blank=True)
    dish = models.ForeignKey(Dish, on_delete=models.DO_NOTHING, null=True, blank=True)
    review = models.TextField()
    rating = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_review_by_dish(dish):
        return Review.objects.filter(dish=dish)

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Review"
    
    def __str__(self):
        return f"ID: {self.id} - Dish: {self.dish.name} - Rating: {self.rating}"


