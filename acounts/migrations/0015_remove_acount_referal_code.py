# Generated by Django 4.2.4 on 2023-10-02 04:41

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("acounts", "0014_alter_referal_code_code"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="acount",
            name="referal_code",
        ),
    ]
