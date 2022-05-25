from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from myadmin.models import Orders, Product


def index(request):
    if not request.session.get('member_is_login', None):  # 已经登录，跳转主页
        message = "请您先完成登录哦！"
        return render(request, 'web/index.html', locals())  # 跳转首页
    # 找到本用户的"未完成交易"订单
    order_list = Orders.objects.filter(member_id=request.session['webuser']['id'])
    if order_list:
        order_list = order_list.filter(status=1)
    whole_price = 0
    for vo in order_list:
        whole_price += vo.whole_price
    whole_price_vip = whole_price * 0.88
    return render(request, "web/cart.html", locals())

def add(request,pid):
    product = Product.objects.get(id=pid)
    order = Orders.objects.filter(product_id=pid) # 找到存在于购物车里面的那一个菜品(但可能交易完成，也可能取消交易)
    order = order.filter(member_id=request.session['webuser']['id']) # 这个用户的订单
    try:
        order = order.get(status=1)  # 找到还没完成交易的那一个，使其数量加一
        order.num = order.num+1
        order.whole_price += order.price
        order.update_at = datetime.now()
        order.save()
    except:                            # 之前没有，则新建这个交易
        order = Orders()
        order.num = 1
        order.name = product.name
        order.shop_id = product.shop_id
        order.product_id = pid
        order.member_id = request.session['webuser']['id']
        order.price = product.price
        order.whole_price = order.price
        order.create_at = datetime.now()
        order.update_at = datetime.now()
        order.save()
    info = '增加完成!'
    return redirect(reverse('cart_index'), locals())

def decrease(request,pid):
    order = Orders.objects.filter(product_id=pid) # 找到存在于购物车里面的那一个菜品(但可能交易完成，也可能取消交易)
    order = order.filter(member_id=request.session['webuser']['id'])
    if order:
        order = order.get(status=1)  # 找到还没完成交易的那一个，使其数量减一
        if order.num > 0:
            order.num =order.num - 1
            order.whole_price -= order.price
            order.save()
    info = '减少完成!'
    return redirect(reverse('cart_index'), locals())

def delete(request,pid):
    order = Orders.objects.filter(product_id=pid)
    order = order.filter(member_id=request.session['webuser']['id'])
    order = order.get(status=1)
    order.status = 3
    order.save()
    info = '删除完成!'
    return redirect(reverse('cart_index'), locals())

def clear(request):
    order = Orders.objects.filter(member_id=request.session['webuser']['id'])
    for vo in order:
        vo.status = 3
        vo.save()
    info = '清空完成！'
    return redirect(reverse('cart_index'),locals())

def add_to_cart(request,pid):
    if not request.session.get('member_is_login', None):
        message = "请您先完成登录哦！"
        return render(request, 'web/index.html', locals())  # 跳转首页
    product = Product.objects.get(id=pid)
    order = Orders.objects.filter(product_id=pid) # 找到存在于购物车里面的那一个菜品(但可能交易完成，也可能取消交易)
    order = order.filter(member_id=request.session['webuser']['id']) # 这个用户的订单
    try:
        order = order.get(status=1)  # 找到还没完成交易的那一个，使其数量加一
        order.num = order.num+1
        order.whole_price += order.price
        order.update_at = datetime.now()
        order.save()
    except:                            # 之前没有，则新建这个交易
        order = Orders()
        order.num = 1
        order.name = product.name
        order.shop_id = product.shop_id
        order.shop_name = product.shop_name
        order.product_id = pid
        order.member_id = request.session['webuser']['id']
        order.price = product.price
        order.whole_price = order.price
        order.create_at = datetime.now()
        order.update_at = datetime.now()
        order.save()
    info = '成功加入购物车!'
    return redirect(reverse('web_menu'), locals())
