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

    @staticmethod 
    def get_order_by_user(user):
        return Order.objects.filter(customer=user)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Order"

    def __str__(self):
        return f"ID: {self.id} - ITEM: {self.customer.admin.username} - TOTAL PRICE: {self.total_price}"


class OrderDish(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='id')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.DO_NOTHING, null=True, blank=True)
    status = models.CharField(default='Đang chờ xử lý', choices=ORDER_STATUS, max_length=31)
    
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING, null=True, blank=True)
    
    delivery_address = models.TextField()
    phone_number = models.CharField(max_length=20) # tham khảo các app đặt đồ nó lấy luôn số điện thoại của người dùng hay cho nhập
    
    dish = models.ForeignKey(Dish, on_delete=models.DO_NOTHING, null=True, blank=True)
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=1)
    note = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(null=True, blank=True)

    @staticmethod
    def get_order_dish_by_order(order):
        return OrderDish.objects.filter(order=order)
    
    @staticmethod
    def get_total_order_of_restaurant_every_day(restaurant):
        now = timezone.now()
        start_of_today = datetime(now.year, now.month, now.day, 0, 0, 0, tzinfo=timezone.get_current_timezone())
        return [OrderDish.objects.filter(
                restaurant=restaurant,
                created_at__gte=start_of_today
            ).count(), OrderDish.objects.filter(
                restaurant=restaurant,
                created_at__gte=start_of_today
            ).order_by('-created_at')]

    @staticmethod
    def get_total_order_of_restaurant_completed_every_day(restaurant):
        now = timezone.now()
        start_of_today = datetime(now.year, now.month, now.day, 0, 0, 0, tzinfo=timezone.get_current_timezone())
        completed_orders = OrderDish.objects.filter(
            restaurant=restaurant,
            status="Hoàn thành",
            created_at__gte=start_of_today
        )
        total_order = completed_orders.count()
        total_price = 0 
        if completed_orders.exists():
            for item in completed_orders:
                total_price += item.price
        return [total_order, total_price]

    @staticmethod
    def get_total_order_cancel(restaurant):
        now = timezone.now()
        start_of_today = datetime(now.year, now.month, now.day, 0, 0, 0, tzinfo=timezone.get_current_timezone())
        total_cancel_orders = OrderDish.objects.filter(
            restaurant=restaurant,
            status="Đã hủy",
            created_at__gte=start_of_today
        ).count()
        return total_cancel_orders

    class Meta:
        verbose_name = "OrderDish"
        verbose_name_plural = "OrderDish"

    def __str__(self):
        return f"{self.id} - FROM {self.restaurant.name} TO {self.order.customer.admin.username} PRICE {self.price} STATUS {self.status} AT {self.created_at}"

