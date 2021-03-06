# Generated by Django 3.2.4 on 2022-05-17 18:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_id', models.IntegerField()),
                ('name', models.CharField(max_length=50)),
                ('types', models.IntegerField()),
                ('status', models.IntegerField(default=1)),
                ('create_at', models.DateTimeField(default=datetime.datetime.now)),
                ('update_at', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'db_table': 'category',
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=50, verbose_name='您的昵称')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='登录账号')),
                ('password_hash', models.CharField(max_length=100)),
                ('password_salt', models.CharField(max_length=50)),
                ('avatar', models.CharField(max_length=255)),
                ('mobile', models.CharField(max_length=50)),
                ('money', models.CharField(default='0', max_length=50)),
                ('address', models.CharField(default='暂无', max_length=255)),
                ('is_vip', models.IntegerField(default=0)),
                ('status', models.IntegerField(default=1)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='邮箱')),
                ('create_at', models.DateTimeField(default=datetime.datetime.now)),
                ('update_at', models.DateTimeField(default=datetime.datetime.now)),
                ('introduce', models.TextField(default='这个人太懒了，什么都没有留下', verbose_name='个人简介')),
            ],
            options={
                'db_table': 'member',
            },
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.IntegerField()),
                ('product_id', models.IntegerField()),
                ('product_name', models.CharField(max_length=50)),
                ('price', models.FloatField()),
                ('quantity', models.IntegerField()),
                ('status', models.IntegerField(default=1)),
            ],
            options={
                'db_table': 'order_detail',
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('shop_id', models.IntegerField()),
                ('product_id', models.IntegerField()),
                ('member_id', models.IntegerField()),
                ('price', models.FloatField()),
                ('num', models.IntegerField(default=0)),
                ('status', models.IntegerField(default=1)),
                ('payment_status', models.IntegerField(default=1)),
                ('create_at', models.DateTimeField(default=datetime.datetime.now)),
                ('update_at', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'db_table': 'orders',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.IntegerField()),
                ('member_id', models.IntegerField()),
                ('money', models.FloatField()),
                ('type', models.IntegerField()),
                ('bank', models.IntegerField(default=1)),
                ('status', models.IntegerField(default=1)),
                ('create_at', models.DateTimeField(default=datetime.datetime.now)),
                ('update_at', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'db_table': 'payment',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_id', models.IntegerField()),
                ('category_id', models.IntegerField()),
                ('cover_pic', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('price', models.FloatField()),
                ('status', models.IntegerField(default=1)),
                ('is_special', models.IntegerField(default=0)),
                ('types', models.IntegerField(default=1)),
                ('sales', models.BigIntegerField(default=0)),
                ('info', models.CharField(default='   ', max_length=50)),
                ('create_at', models.DateTimeField(default=datetime.datetime.now)),
                ('update_at', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'db_table': 'product',
            },
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('cover_pic', models.CharField(max_length=255)),
                ('banner_pic', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=255)),
                ('status', models.IntegerField(default=1)),
                ('create_at', models.DateTimeField(default=datetime.datetime.now)),
                ('update_at', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'db_table': 'shop',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('nickname', models.CharField(max_length=50)),
                ('password_hash', models.CharField(max_length=100)),
                ('password_salt', models.CharField(max_length=50)),
                ('status', models.IntegerField(default=1)),
                ('create_at', models.DateTimeField(default=datetime.datetime.now)),
                ('update_at', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]
