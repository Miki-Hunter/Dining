# Generated by Django 3.2.4 on 2022-05-19 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0003_orders_whole_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='cost',
            field=models.FloatField(default=0),
        ),
    ]
