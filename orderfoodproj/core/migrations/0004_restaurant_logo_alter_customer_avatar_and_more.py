# Generated by Django 4.2.9 on 2024-04-13 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_provider_id_card_provider_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='logo',
            field=models.ImageField(default='default/logo.png', upload_to='rest-logo/'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='avatar',
            field=models.ImageField(default='default/user.png', upload_to='uploads/user_avatar/'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='banner',
            field=models.ImageField(default='default/banner.png', upload_to='banners/'),
        ),
    ]
