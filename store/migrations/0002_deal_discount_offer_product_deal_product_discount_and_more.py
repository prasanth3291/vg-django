# Generated by Django 4.2.4 on 2023-09-23 03:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Deal",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("discount", models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Discount",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("discount", models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Offer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("description", models.TextField()),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                (
                    "discount",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="store.discount"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="product",
            name="deal",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="store.deal",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="discount",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="store.discount",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="offer",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="store.offer",
            ),
        ),
    ]
