# Generated by Django 4.2.4 on 2023-09-26 12:11

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("acounts", "0008_coupons_coupon_count"),
    ]

    operations = [
        migrations.RenameField(
            model_name="coupons",
            old_name="maxium_discount",
            new_name="maximum_discount",
        ),
        migrations.RenameField(
            model_name="coupons",
            old_name="mininum_amount",
            new_name="minimum_amount",
        ),
    ]
