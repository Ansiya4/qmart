# Generated by Django 4.2.1 on 2023-06-04 08:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_rename_colors_product_color_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='color_name',
        ),
        migrations.AddField(
            model_name='product',
            name='color_name',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='product.colorvariation'),
        ),
    ]
