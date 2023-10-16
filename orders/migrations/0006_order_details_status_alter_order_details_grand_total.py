# Generated by Django 4.2.4 on 2023-10-05 17:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0005_order_details"),
    ]

    operations = [
        migrations.AddField(
            model_name="order_details",
            name="status",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="order_details",
            name="grand_total",
            field=models.FloatField(),
        ),
    ]
