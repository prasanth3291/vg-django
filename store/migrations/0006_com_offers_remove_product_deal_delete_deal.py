# Generated by Django 4.2.4 on 2023-10-04 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_delete_reviewrating'),
    ]

    operations = [
        migrations.CreateModel(
            name='com_offers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('discount', models.PositiveIntegerField()),
                ('description', models.TextField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='deal',
        ),
        migrations.DeleteModel(
            name='Deal',
        ),
    ]