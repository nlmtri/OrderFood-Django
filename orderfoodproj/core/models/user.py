from django.db import models

from django.contrib.auth.models import AbstractUser 
from django.db.models.signals import post_save 
from django.dispatch import receiver 

from .restaurant import Restaurant
from .city import City


class CustomUser(AbstractUser):
    user_type_data = (
        (1, "customer"),
        (2, "provider"),
    )
    user_type = models.CharField(default=1, choices=user_type_data, max_length=15)


class Customer(models.Model):
    '''Khách hàng'''
    
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='id')
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    
    address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    avatar = models.ImageField(upload_to='uploads/user_avatar/', default='default/user.png')
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING, null=True, blank=True) # nếu có địa chỉ lọc theo thành phố

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.id}-{self.admin.username}"
    

class Provider(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='id')
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    restaurant = models.ForeignKey(Restaurant, on_delete=models.DO_NOTHING, null=True, blank=True)


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    '''
    sender: class gọi đến hàm này
    instance: là dữ liệu đang chèn vào model
    created: là True/False, True khi data được chèn vào
    '''
    if created:
        if instance.user_type == 1:
            Customer.objects.create(admin=instance)
        if instance.user_type == 2:
            Provider.objects.create(admin=instance)
        if instance.user_type == 3:
            Staff.objects.create(admin=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    '''Phương thức này sẽ được gọi sau khi create_user_profile được thực thi'''
    if instance.user_type == 1:
        instance.customer.save()
    if instance.user_type == 2:
        instance.provider.save()
    if instance.user_type == 3:
        instance.staff.save()
