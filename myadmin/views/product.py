import os
import time
from datetime import datetime
from django.utils import timezone as datetime
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render

from myadmin.models import Product, Shop, Category
from Dining.settings import PROJECT_ROOT


def index(request, pIndex=1):
    smod = Product.objects
    mywhere = []
    # 排除掉已经删除的店铺
    list = smod.filter(status__lt=9)
    # 获取、判断并封装关keyword键搜索
    kw = request.GET.get("keyword", None)
    if kw:
        # 查询店铺名称中只要含有关键字就可以
        list = list.filter(name__contains=kw)
        mywhere.append("keyword=" + kw)
    # 获取、判断并封装状态status搜索条件
    status = request.GET.get('status', '')
    if status != '':
        list = list.filter(status=status)
        mywhere.append("status=" + status)
    # 执行分页处理
    pIndex = int(pIndex)
    page = Paginator(list, 5)  # 以5条每页创建分页对象
    maxpages = page.num_pages  # 最大页数
    # 判断页数是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)  # 当前页数据
    plist = page.page_range  # 页码数列表
    # 封装信息加载模板输出
    for vo in list2:
        vo.shopname = Shop.objects.get(id=vo.shop_id).name
        vo.categoryname = Category.objects.get(id=vo.category_id).name

    # 封装信息加载模板输出
    context = {"productlist": list2, 'plist': plist, 'pIndex': pIndex, 'maxpages': maxpages, 'mywhere': mywhere}
    return render(request, "myadmin/product/index.html", context)


def found(request, cid):
    if cid == 7:          # 特殊情况： “特色菜” 不是一种菜的类别，所有菜都可能成为特色菜   即is_special=1
        list1 = Product.objects.filter(is_special=1)
    else:
        list1 = Product.objects.filter(category_id=cid)
    mywhere=[]
    # 执行分页处理
    pIndex = 1
    page = Paginator(list1, 5) # 以5条每页创建分页对象
    maxpages = page.num_pages # 最大页数
    #判断页数是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex) #当前页数据
    plist = page.page_range   #页码数列表
    for vo in list2:
        vo.shopname = Shop.objects.get(id=vo.shop_id).name
        vo.categoryname = Category.objects.get(id=vo.id).name
    context = {"productlist": list2, 'plist': plist, 'pIndex': pIndex, 'maxpages': maxpages, 'mywhere': mywhere}
    return render(request, "myadmin/product/index.html", context)


def add(request):
    """加载添加页面"""
    slist = Shop.objects.values("id", "name")
    context = {"shoplist": slist}
    return render(request, "myadmin/product/add.html", context)


def insert(request):
    """执行添加"""
    try:
        # 图片的上传处理
        myfile = request.FILES.get("cover_pic", None)
        if not myfile:
            return HttpResponse("没有封面上传文件信息")
        cover_pic = str(time.time()) + "." + myfile.name.split('.').pop()
        destination = open(PROJECT_ROOT + "/static/uploads/product/" + cover_pic, "wb+")
        for chunk in myfile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        # 实例化model，封装信息，并执行添加
        ob = Product()
        ob.info = request.POST['info1']+' '+request.POST['info2']+' '+request.POST['info3']+' '+request.POST['info4']
        ob.shop_id = request.POST['shop_id']
        ob.category_id = request.POST['category_id']
        ob.types = Category.objects.get(id=ob.category_id).types
        ob.name = request.POST['name']
        ob.price = request.POST['price']
        ob.shop_name = Shop.objects.get(id=ob.shop_id).name
        ob.cover_pic = cover_pic
        ob.status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {"info": "添加成功！"}
    except Exception as err:
        print(err)
        context = {"info": "添加失败"}
    return render(request, "myadmin/info.html", context)


def delete(request, pid):
    """删除信息"""
    try:
        ob = Product.objects.get(id=pid)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {"info": "删除成功！"}
    except Exception as err:
        print(err)
        context = {"info": "删除失败"}
    return JsonResponse(context)


def edit(request, pid):
    """加载编辑信息页面"""
    try:
        ob = Product.objects.get(id=pid)
        slist = Shop.objects.values("id", "name")
        infolist = ob.info.split(' ')
        context = {"product": ob, "shoplist": slist,'infolist':infolist}
        return render(request, "myadmin/product/edit.html", context)
    except Exception as err:
        context = {"info": "没有找到要修改的信息！"}
        # return JsonResponse(context)
        return render(request, "myadmin/info.html", context)


def update(request, pid):
    """执行编辑信息"""
    try:
        ob = Product.objects.get(id=pid)# 获取原图片名
        oldpicname = ob.cover_pic
        myfile = request.FILES.get("cover_pic_new", None)
        if not myfile:
            cover_pic = oldpicname
        else:  # 判断是否有文件上传
            cover_pic = str(time.time()) + "." + myfile.name.split('.').pop()
            destination = open(PROJECT_ROOT + "/static/uploads/product/" + cover_pic, "wb+")
            for chunk in myfile.chunks():  # 分块写入文件
                destination.write(chunk)
            destination.close()
            # 删除旧文件
            os.remove(PROJECT_ROOT + "/static/uploads/product/" + oldpicname)

        ob.info = request.POST['1'] + ' ' + request.POST['2'] + ' ' + request.POST['3'] + ' ' + request.POST['4']
        ob.shop_id = request.POST['shop_id']
        ob.shop_name = Shop.objects.get(id=request.POST['shop_id']).name
        ob.category_id = request.POST['category_id']
        ob.name = request.POST['name']
        ob.price = float(request.POST['price'])
        ob.cover_pic = cover_pic
        ob.status = request.POST['status']
        ob.is_special = request.POST['is_special']
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {"info": "修改成功！"}

    except Exception as err:
        print(err)
        context = {"info": "修改失败"}
    return render(request, "myadmin/info.html", context)



