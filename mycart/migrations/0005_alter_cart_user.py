# Generated by Django 4.2.2 on 2023-07-06 06:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loginSystem', '0003_account_wallet'),
        ('mycart', '0004_alter_cart_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='loginSystem.account'),
        ),
    ]
