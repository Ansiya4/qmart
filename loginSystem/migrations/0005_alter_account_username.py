# Generated by Django 4.2.2 on 2023-07-13 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginSystem', '0004_alter_account_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='username',
            field=models.CharField(max_length=50),
        ),
    ]