# Generated by Django 4.2.4 on 2023-10-03 03:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_reviewrating'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ReviewRating',
        ),
    ]