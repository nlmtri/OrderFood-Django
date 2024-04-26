from django.db import models 
from .user import Customer
from .restaurant import Restaurant
from .dish import Dish

from django.utils import timezone 
from datetime import datetime, timedelta 


ORDER_STATUS = (
    ('Đang chờ xử lý', 'Đang chờ xử lý'),
    ('Đã tiếp nhận', 'Đã tiếp nhận'),
    ('Đang giao', 'Đang giao'),
    ('Hoàn thành', 'Hoàn thành'),
    ('Đã hủy', 'Đã hủy')
)


class Order(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='id')
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, null=True, blank=True)
    total_price = models.IntegerField(default=0)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.DO_NOTHING, null=True, blank=True)
    status = models.CharField(default='Đang chờ xử lý', choices=ORDER_STATUS, max_length=31)
    delivery_address = models.TextField(default='')
    phone_number = models.CharField(max_length=20, default='')
    created_at = models.DateTimeField(null=True, blank=True)

    @staticmethod 
    def get_order_by_user(user):
        return Order.objects.filter(customer=user)
    
    @staticmethod
    def get_total_order_of_restaurant(restaurant):
        now = timezone.now()
        return [Order.objects.filter(
                restaurant=restaurant,
            ).count(), Order.objects.filter(
                restaurant=restaurant,
            ).order_by('-created_at')]

    @staticmethod
    def get_total_order_of_restaurant_completed(restaurant):
        completed_orders = Order.objects.filter(
            restaurant=restaurant,
            status="Hoàn thành",
        )
        total_order = completed_orders.count()
        total_price = 0 
        if completed_orders.exists():
            for item in completed_orders:
                total_price += item.total_price
        return [total_order, total_price]

    @staticmethod
    def get_total_order_cancel(restaurant):
        total_cancel_orders = Order.objects.filter(
            restaurant=restaurant,
            status="Đã hủy"
        ).count()
        return total_cancel_orders

    def __str__(self):
        return f"ID: {self.id} - FROM {self.restaurant.name} TO {self.order.customer.admin.username} PRICE {self.total_price} STATUS {self.status} AT {self.created_at}"


class OrderDish(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='id')
    
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING, null=True, blank=True)
    
    dish = models.ForeignKey(Dish, on_delete=models.DO_NOTHING, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    note = models.TextField(null=True, blank=True)

    @staticmethod
    def get_order_dish_by_order(order):
        return OrderDish.objects.filter(order=order)

    def __str__(self):
        return f"{self.id} - FROM {self.restaurant.name} TO {self.order.customer.admin.username} PRICE {self.price} STATUS {self.status} AT {self.created_at}"

