# Generated by Django 4.2.4 on 2023-09-24 06:54

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0002_usercoupons"),
    ]

    operations = [
        migrations.DeleteModel(
            name="UserCoupons",
        ),
    ]
