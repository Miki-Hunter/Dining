from datetime import datetime

from django.core.paginator import Paginator
from django.shortcuts import render
from myadmin.models import User, Member, Orders

def orders_today(request,pIndex=1):
    today = datetime.now().date()
    orders = Orders.objects.filter(update_at__gt=today)
    orders = orders.order_by('-update_at')

    #执行分页处理
    pIndex = int(pIndex)
    page = Paginator(orders,8) #以5条每页创建分页对象
    maxpages = page.num_pages #最大页数
    #判断页数是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex) #当前页数据
    plist = page.page_range   #页码数列表
    #封装信息加载模板输出
    context = {"orders_list":list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages}
    return render(request, 'myadmin/orders.html', context)

def orders_all(request,pIndex=1):
    orders = Orders.objects.order_by('-update_at')
    #执行分页处理
    pIndex = int(pIndex)
    page = Paginator(orders,8) #以5条每页创建分页对象
    maxpages = page.num_pages #最大页数
    #判断页数是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex) #当前页数据
    plist = page.page_range   #页码数列表
    #封装信息加载模板输出
    context = {"orders_list":list2,'plist_all':plist,'pIndex_all':pIndex,'maxpages_all':maxpages}
    return render(request, 'myadmin/orders.html',context)