# Generated by Django 4.2.2 on 2023-07-13 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginSystem', '0005_alter_account_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='user_image',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='photos/profile'),
        ),
    ]
