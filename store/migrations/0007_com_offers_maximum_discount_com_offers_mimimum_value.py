# Generated by Django 4.2.4 on 2023-10-05 07:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0006_com_offers_remove_product_deal_delete_deal"),
    ]

    operations = [
        migrations.AddField(
            model_name="com_offers",
            name="maximum_discount",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="com_offers",
            name="mimimum_value",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
