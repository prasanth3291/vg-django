# Generated by Django 4.2.4 on 2023-09-07 08:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0005_alter_cartitem_date_added'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='date_added',
        ),
    ]
