# Generated by Django 4.2.4 on 2023-10-01 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acounts', '0012_acount_wallet_money_alter_wishlist_added_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='acount',
            name='referal_code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]