# Generated by Django 4.2.1 on 2023-06-04 03:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_colorvariation_product_colors'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='colors',
            new_name='color_name',
        ),
    ]
