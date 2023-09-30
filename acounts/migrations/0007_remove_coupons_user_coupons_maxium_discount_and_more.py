# Generated by Django 4.2.4 on 2023-09-26 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acounts', '0006_coupons_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coupons',
            name='user',
        ),
        migrations.AddField(
            model_name='coupons',
            name='maxium_discount',
            field=models.IntegerField(default=5000),
        ),
        migrations.AddField(
            model_name='coupons',
            name='mininum_amount',
            field=models.IntegerField(default=5000),
        ),
    ]
