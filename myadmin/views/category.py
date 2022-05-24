from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from datetime import datetime

from django.urls import reverse

from Dining.settings import PROJECT_ROOT
from django.contrib import messages
from myadmin.models import Category,Shop

# 菜品分类信息

def index(request,pIndex=1):
    """浏览信息"""
    smod = Category.objects
    mywhere=[]
    alist = smod.filter(status__lt=9)

    # 获取、判断并封装关keyword键搜索
    kw = request.GET.get("keyword",None)
    if kw:
        # 查询店铺名称中只要含有关键字就可以
        alist = alist.filter(name__contains=kw)
        mywhere.append("keyword="+kw)

    # 获取、判断并封装状态status搜索条件
    status = request.GET.get('status','')
    if status != '':
        alist = alist.filter(status=status)
        mywhere.append("status="+status)

    #执行分页处理
    pIndex = int(pIndex)
    page = Paginator(alist, 7) #以7条每页创建分页对象
    maxpages = page.num_pages #最大页数
    #判断页数是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex) #当前页数据
    plist = page.page_range   #页码数列表

    #遍历信息，并获取对应的商铺名称，以shopname名封装
    for vo in list2:
        sob = Shop.objects.get(id=vo.shop_id)
        vo.shopname = sob.name
    #封装信息加载模板输出
    context = {"categorylist":list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere}
    return render(request,"myadmin/category/index.html",context)


def loadCategory(request,sid):
    clist = Category.objects.filter(status__lt=9,shop_id=sid).values("id","name")
    #返回QuerySet对象，使用list强转成对应的菜品分类列表信息
    return JsonResponse({'data':list(clist)})


def found(request,sid):
    alist = Category.objects.filter(shop_id=sid)
    mywhere=[]
    # 执行分页处理
    pIndex = 1
    page = Paginator(alist, 7) # 以7条每页创建分页对象
    maxpages = page.num_pages # 最大页数
    #判断页数是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex) #当前页数据
    plist = page.page_range   #页码数列表
    #封装信息加载模板输出
    for vo in list2:
        sob = Shop.objects.get(id=sid)
        vo.shopname = sob.name
    context = {"categorylist":list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere}
    return render(request,"myadmin/category/index.html",context)


def add(request):
    """加载添加页面"""
    slist = Shop.objects.values("id","name")
    context={"shoplist":slist}
    return render(request,"myadmin/category/add.html",context)

def insert(request):
    """执行添加"""
    try:
        ob = Category()
        ob.shop_id = request.POST['shop_id']
        [types,ob.name] = request.POST['name'].split()
        ob.types = int(types)
        ob.status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context={"info":"添加成功！"}
    except Exception as err:
        print(err)
        context={"info":"添加失败"}
    return render(request,"myadmin/info.html",context)


def delete(request,cid):
    """删除信息"""
    try:
        ob = Category.objects.get(id=cid)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context={"info":"删除成功！"}
    except Exception as err:
        print(err)
        context={"info":"删除失败"}
    return JsonResponse(context)


def edit(request,cid):
    """加载编辑信息页面"""
    try:
        ob = Category.objects.get(id=cid)
        slist = Shop.objects.values("id","name")
        context={"category":ob,"shoplist":slist}
        return render(request,"myadmin/category/edit.html",context)
    except Exception as err:
        context={"info":"没有找到要修改的信息！"}
        return render(request,"myadmin/info.html",context)


def update(request,cid):
    """执行编辑信息"""
    try:
        ob = Category.objects.get(id=cid)
        ob.shop_id = request.POST['shop_id']
        ob.name = request.POST['name']
        if request.POST['name']=='早餐':
            ob.types = 1
        elif request.POST['name']=='午餐':
            ob.types = 2
        elif request.POST['name']=='晚餐':
            ob.types = 3
        elif request.POST['name']=='饮料':
            ob.types = 4
        elif request.POST['name']=='沙拉':
            ob.types = 5
        elif request.POST['name']=='甜点':
            ob.types = 6
        else:
            ob.types = 7
        ob.status = request.POST['status']
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context={"info":"修改成功！"}
    except Exception as err:
        print(err)
        context={"info":"修改失败"}

    return render(request,"myadmin/info.html",context)
