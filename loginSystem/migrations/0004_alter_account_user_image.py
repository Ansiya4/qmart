# Generated by Django 4.2.2 on 2023-07-11 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginSystem', '0003_account_wallet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='user_image',
            field=models.ImageField(blank=True, null=True, upload_to='photos/profile'),
        ),
    ]
