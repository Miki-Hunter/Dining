from django.urls import path
from django.conf.urls import url
from django.urls import include

from django.contrib import admin
from myadmin.views import index, user, shop, category, product, member, orders

urlpatterns = [
    path('captcha', include('captcha.urls')),
    path('', index.index, name="myadmin_index"),  # 后台首页
    # 后台管理员登录、退出路由
    path('login', index.login, name="myadmin_login"),  # 加载登录表单
    path('dologin', index.dologin, name="myadmin_dologin"),  # 执行登录
    path('logout', index.logout, name="myadmin_logout"),  # 退出


    #员工账号信息管理
    path('user/<int:pIndex>', user.index, name="myadmin_user_index"),#浏览信息
    path('user/add', user.add, name="myadmin_user_add"),             #加载添加表单
    path('user/insert', user.insert, name="myadmin_user_insert"),     #执行信息添加
    path('user/del/<int:uid>', user.delete, name="myadmin_user_del"),#删除信息
    path('user/edit/<int:uid>', user.edit, name="myadmin_user_edit"),#准备信息编辑
    path('user/update/<int:uid>', user.update, name="myadmin_user_update"),#执行信息编辑


    #重置员工密码
    #path('user/resetpass/<int:uid>', user.resetpass, name="myadmin_user_resetpass"),
    #path('user/doresetpass/<int:uid>', user.doresetpass, name="myadmin_user_doresetpass"),


    # 店铺路由
    path('shop/<int:pIndex>', shop.index, name="myadmin_shop_index"),
    path('shop/add', shop.add, name="myadmin_shop_add"),
    path('shop/insert', shop.insert, name="myadmin_shop_insert"),
    path('shop/del/<int:sid>', shop.delete, name="myadmin_shop_del"),
    path('shop/edit/<int:sid>', shop.edit, name="myadmin_shop_edit"),
    path('shop/update/<int:sid>', shop.update, name="myadmin_shop_update"),

    # 菜品分类信息管理
    path('category/<int:pIndex>', category.index, name="myadmin_category_index"),
    path('category/load/<int:sid>', category.loadCategory, name="myadmin_category_load"),
    path('category/add', category.add, name="myadmin_category_add"),
    path('category/insert', category.insert, name="myadmin_category_insert"),
    path('category/del/<int:cid>', category.delete, name="myadmin_category_del"),
    path('category/edit/<int:cid>', category.edit, name="myadmin_category_edit"),
    path('category/update/<int:cid>', category.update, name="myadmin_category_update"),
    path('category/found/<int:sid>', category.found, name="myadmin_category_found"),


    # 菜品信息管理
    path('product/<int:pIndex>', product.index, name="myadmin_product_index"),
    path('product/add', product.add, name="myadmin_product_add"),
    path('product/insert', product.insert, name="myadmin_product_insert"),
    path('product/del/<int:pid>', product.delete, name="myadmin_product_del"),
    path('product/edit/<int:pid>', product.edit, name="myadmin_product_edit"),
    path('product/update/<int:pid>', product.update, name="myadmin_product_update"),
    path('product/found/<int:cid>', product.found, name="myadmin_product_found"),

    # 会员管理路由
    path('member/<int:pIndex>', member.index, name="myadmin_member_index"),  # 浏览会员
    path('member/member_today/<int:pIndex>', member.today_member, name="today_member"),  # 浏览会员
    path('member/vip_member_today/<int:pIndex>', member.today_vip_member, name="today_vip_member"),  # 浏览会员
    path('member/add', member.add, name="myadmin_member_add"),
    path('member/insert', member.insert, name="myadmin_member_insert"),
    path('member/del/<int:sid>', member.delete, name="myadmin_member_del"),
    path('member/edit/<int:sid>', member.edit, name="myadmin_member_edit"),
    path('member/update/<int:sid>', member.update, name="myadmin_member_update"),

    # 订单
    path('orders/today/<int:pIndex>', orders.orders_today, name="myadmin_orders_today"),
    path('orders/all/<int:pIndex>', orders.orders_all, name="myadmin_orders_all"),


]
"""
alter table member change member_id int(11) not null AUTO_INCREMENT;
"""
