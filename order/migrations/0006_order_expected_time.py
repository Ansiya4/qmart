# Generated by Django 4.2.2 on 2023-06-21 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_alter_order_mode_of_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='expected_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
