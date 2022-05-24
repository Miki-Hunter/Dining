from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.core.paginator import Paginator
from datetime import datetime

from myadmin.models import User,Shop,Category,Product,Orders,OrderDetail,Payment

def index(request,pIndex=1):
    if not request.session.get('member_is_login', None):
        message = "请您先完成登录哦！"
        return render(request, 'web/index.html', locals())  # 跳转首页
    # 找到本用户的"已完成交易"订单
    order_list = Orders.objects.filter(member_id=request.session['webuser']['id'])
    if order_list:
        order_list = order_list.filter(payment_status=2)
    #执行分页处理
    pIndex = int(pIndex)
    page = Paginator(order_list,5) #以5条每页创建分页对象
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
    return render(request, "web/orders.html", context)

def insert(request):
    """大堂执行订单添加操作"""
    try:
        # 执行订单信息添加操作
        od = Orders()
        od.shop_id = request.session['shopinfo']['id'] #店铺id号
        od.member_id = 0 #会员id
        od.user_id = request.session['webuser']['id'] #操作员id
        od.money = request.session['total_money']
        od.status = 1 #订单状态:1过行中/2无效/3已完成
        od.payment_status = 2 #支付状态:1未支付/2已支付/3已退款
        od.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        od.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        od.save()

        # 执行支付信息添加
        op = Payment()
        op.order_id = od.id #订单id号
        op.member_id = 0 #会员id号
        op.money = request.session['total_money'] #支付款
        op.type = 2 #付款方式：1会员付款/2收银收款
        op.bank = request.GET.get("bank",3) #收款银行渠道:1微信/2余额/3现金/4支付宝
        op.status = 2 #支付状态:1未支付/2已支付/3已退款
        op.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        op.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        op.save()

        # 执行订单详情添加
        cartlist = request.session.get('cartlist',{})
        for shop in cartlist.values():
            ov = OrderDetail()
            ov.order_id = od.id
            ov.product_id = shop['id']
            ov.product_name = shop['name']
            ov.price = shop['price']
            ov.quantity = shop['num']
            ov.status = 1
            ov.save()
        del request.session['cartlist']
        del request.session['total_money']
        return HttpResponse("Y")
    except Exception as err:
        print(err)
        context = {"info":"订单添加失败，请稍后再试！"}
        return HttpResponse("N")

def detail(request):
    """加载订单信息"""
    oid = request.GET.get("oid",0)

    # 加载订单详情
    dlist = OrderDetail.objects.filter(order_id=oid)
    # 遍历每个商品详情，从Goods中获取对应的图片
    #for og in dlist:
    #    og.picname = Goods.objects.only('picname').get(id=og.goodsid).picname

    # 放置模板变量，加载模板并输出
    context = {'detaillist':dlist}
    return render(request,"web/details.html",context)

def status(request):
    """ 修改订单状态 """
    try:
        oid = request.GET.get("oid",'0')
        ob = Orders.objects.get(id=oid)
        ob.status = request.GET['status']
        ob.save()
        return HttpResponse("Y")
    except Exception as err:
        print(err)
        return HttpResponse("N")