# Generated by Django 4.2.4 on 2023-09-07 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='carts',
            name='date_added',
            field=models.DateField(auto_now_add=True),
        ),
    ]