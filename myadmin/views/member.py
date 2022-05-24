import os
import random
import hashlib
import re

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from datetime import datetime
from decimal import Decimal
import time
from Dining.settings import PROJECT_ROOT
from myadmin import models
from myadmin.form import MemberForm
from myadmin.models import Member

# ==============后台会员信息管理======================
# 浏览会员信息
def index(request,pIndex=1):
    mmod = Member.objects
    mywhere = []
    list = mmod.filter(status__lt=9)
    # 获取、判断并封装关keyword键搜索
    kw = request.GET.get("keyword",None)
    if kw:
        # 查询店铺名称中只要含有关键字就可以
        list = list.filter(nickname__contains=kw)
        mywhere.append("keyword="+kw)

    # 获取、判断并封装状态status搜索条件
    status = request.GET.get('status', '')
    if status != '':
        list = list.filter(status=status)
        mywhere.append("status=" + status)

    #执行分页处理
    pIndex = int(pIndex)
    page = Paginator(list,5) #以5条每页创建分页对象
    maxpages = page.num_pages #最大页数
    #判断页数是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex) #当前页数据
    plist = page.page_range   #页码数列表
    #封装信息加载模板输出
    context = {"member_list":list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages}
    return render(request,"myadmin/member/index.html",context)

def today_member(request,pIndex=1):
    today = datetime.now().date()
    member_list = Member.objects.filter(create_at__gt=today)
    pIndex = int(pIndex)
    page = Paginator(member_list,5) #以5条每页创建分页对象
    maxpages = page.num_pages #最大页数
    #判断页数是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex) #当前页数据
    plist = page.page_range   #页码数列表
    #封装信息加载模板输出
    context = {"member_list":list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages}
    return render(request,"myadmin/member/index.html",context)

def today_vip_member(request,pIndex=1):
    today = datetime.now().date()
    member_list = Member.objects.filter(create_at__gt=today)
    member_list = member_list.filter(is_vip=1)      # 查询VIP用户
    pIndex = int(pIndex)
    page = Paginator(member_list,5) #以5条每页创建分页对象
    maxpages = page.num_pages #最大页数
    #判断页数是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex) #当前页数据
    plist = page.page_range   #页码数列表
    #封装信息加载模板输出
    context = {"member_list":list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages}
    return render(request,"myadmin/member/index.html",context)

def add(request):
    """加载添加页面"""
    return render(request,"myadmin/member/add.html",locals())

def insert(request):
    """执行添加"""
    try:
        # 头像
        massage = ''
        myfile = request.FILES.get("avatar",None)
        if not myfile:
            return HttpResponse("没有会员上传文件信息！")
        cover_pic = str(time.time())+"."+myfile.name.split('.').pop()
        destination = open(PROJECT_ROOT+"/static/uploads/member/"+cover_pic,"wb")
        for chunk in myfile.chunks():      # 分块写入文件
            destination.write(chunk)
        destination.close()
        same_name_user = models.Member.objects.filter(name=request.POST['membername'])
        same_email_user = models.Member.objects.filter(email=request.POST['email'])
        if len(request.POST['membername']) > 9:
            message = "您的昵称太长！"
        elif len(request.POST['password1']) < 8 or len(request.POST['password1']) > 20:
            message = "请输入8~20位密码哦！"
        elif request.POST['password1'] != request.POST['password2']:
            message = "两次输入的密码不同！"
        elif same_name_user:  # 用户名唯一
            message = '用户已经存在，请重新选择用户名！'
        elif same_email_user:  # 邮箱地址唯一
            message = '该邮箱地址已被注册，请使用别的邮箱！'
        else:
            ob = Member()
            ob.nickname = request.POST['nickname']
            ob.name = request.POST['membername']
            ob.mobile = request.POST['mobile']
            ob.address = request.POST['address']
            ob.email = request.POST['email']
            md5 = hashlib.md5()
            n = random.randint(100000, 999999)
            s = request.POST['password1'] + str(n)
            ob.password_salt = n
            md5.update(s.encode('utf-8'))
            ob.password_hash = md5.hexdigest()
            ob.avatar = cover_pic
            ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ob.save()
            message = '添加成功！'
    except Exception as err:
        print(err)
        message = '添加失败！'
    return render(request,"myadmin/member/add.html",locals())

def delete(request,sid):
    """删除信息"""
    try:
        ob = Member.objects.get(id=sid)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context={"info":"删除成功！"}
    except Exception as err:
        print(err)
        context={"info":"删除失败"}
    return render(request,"myadmin/info.html",context)

def edit(request,sid):
    """加载编辑信息页面"""
    try:
        ob = Member.objects.get(id=sid)
        context={"member":ob}
        return render(request,"myadmin/member/edit.html",context)
    except Exception as err:
        context={"info":"没有找到要修改的信息！"}
        return render(request,"myadmin/info.html",context)

def update(request,sid):
    """执行编辑信息"""
    try:
        ob = Member.objects.get(id=sid)
        oldpicname = ob.avatar
        myfile = request.FILES.get("avatar", None)
        if not myfile:
            avatar = oldpicname
        else:  # 判断是否有文件上传
            avatar = str(time.time()) + "." + myfile.name.split('.').pop()
            destination = open(PROJECT_ROOT + "/static/uploads/member/" + avatar, "wb+")
            for chunk in myfile.chunks():  # 分块写入文件
                destination.write(chunk)
            destination.close()
            # 删除旧文件
            os.remove(PROJECT_ROOT + "/static/uploads/member/" + oldpicname)
        ob.nickname = request.POST['nickname']
        ob.mobile = request.POST['mobile']
        ob.address = request.POST['address']
        ob.status = request.POST['status']
        ob.avatar = avatar
        ob.is_vip= request.POST['is_vip']
        if request.POST['is_vip'] == '1':
            ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if request.POST['money']:
            money = float(request.POST['money'])
        else:
            money = 0.0
        ob.money = str(float(ob.money) + money)   # 保留小数点后2位
        if request.POST['is_reset']=="1":
            md5 = hashlib.md5()
            s = ob.name + ob.password_salt
            md5.update(s.encode('utf-8'))
            ob.password_hash = md5.hexdigest()
        ob.save()
        context={"info":"修改成功！"}
    except Exception as err:
        print(err)
        context={"info":"修改失败"}
    return render(request,"myadmin/info.html",context)