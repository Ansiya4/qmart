# Generated by Django 4.2.1 on 2023-06-04 08:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_remove_product_color_name_product_color_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='color_name',
            field=models.ForeignKey(default='No color', on_delete=django.db.models.deletion.CASCADE, to='product.colorvariation'),
        ),
    ]
