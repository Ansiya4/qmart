# Generated by Django 4.2.2 on 2023-06-20 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_alter_order_mode_of_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='mode_of_payment',
            field=models.CharField(blank=True, default=1, max_length=50),
            preserve_default=False,
        ),
    ]
