# Generated by Django 4.2.2 on 2023-06-23 06:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coupon',
            old_name='min_price_amount',
            new_name='min_price',
        ),
    ]
