# Generated by Django 4.2.11 on 2024-04-19 18:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_remove_orderdish_created_at_order_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='provider',
            name='ID_card',
        ),
        migrations.RemoveField(
            model_name='provider',
            name='address',
        ),
        migrations.RemoveField(
            model_name='provider',
            name='business_license',
        ),
        migrations.RemoveField(
            model_name='provider',
            name='business_number',
        ),
        migrations.RemoveField(
            model_name='provider',
            name='date_of_birth',
        ),
        migrations.RemoveField(
            model_name='provider',
            name='food_safty_cert',
        ),
        migrations.RemoveField(
            model_name='provider',
            name='fullname',
        ),
        migrations.RemoveField(
            model_name='provider',
            name='phone',
        ),
    ]
