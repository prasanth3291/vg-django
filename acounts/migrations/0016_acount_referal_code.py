# Generated by Django 4.2.4 on 2023-10-02 04:42

import acounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acounts', '0015_remove_acount_referal_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='acount',
            name='Referal_code',
            field=models.CharField(default=acounts.models.generate_unique_referral_code, max_length=6, unique=True),
        ),
    ]
