import json
import random
from datetime import datetime
from Dining.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings


from myadmin.models import User, Shop, Category, Product, Member, Orders

# 前台首页
def index(request):
    # request.session.flush()
    info = ''
    message = ''
    if request.method == "POST":
        vo = Member.objects.get(id=request.session['webuser']['id'])
        money = float(vo.money)
        whole_price = float(request.POST['whole_price'])
        if vo.is_vip == 1:
            whole_price =whole_price*0.88
        if money >= whole_price:
            if vo.is_vip == 1:
                message = message + "由于您是尊贵的VIP，本次订单享受8.8折优惠！折后价为:%.2f元" % whole_price
            else:
                message = message + "您本次消费:%.2f元" % whole_price
            money -= whole_price
            vo.money = '%.2f' %money
            vo.cost += float("%.2f" % whole_price)
            if vo.cost >= 2000 and vo.is_vip == 0:  # 累销 2000可以成为VIP
                vo.is_vip = 1
                vo.create_at = datetime.now()
                vo.update_at = datetime.now()
                message = message + "\n您的累计消费超过2000,已成功升级为VIP用户!"
            request.session['webuser'] = vo.toDict()
            vo.save()
            order_list = Orders.objects.filter(member_id=request.session['webuser']['id'])
            if order_list:
                order_list = order_list.filter(status=1)  # 未支付订单
            for vo in order_list:
                po=Product.objects.get(id=vo.product_id)
                po.sales += vo.num
                po.save()
                vo.payment_status = 2
                vo.status = 3
                vo.whole_price *= 0.88
                vo.save()
            message = message + "\n订单交易成功！祝您用餐愉快哦！"
        else:
            info = "很可惜，您的余额不足！请您先充值哦！"
    return render(request, 'web/index.html',locals())

def menu(request):
    mod = Product.objects
    whole_list = mod.filter(status__lt=9)   # 只搜索在售的有效菜品
    breakfast = whole_list.filter(types=1)
    lunch = whole_list.filter(types=2)
    dinner = whole_list.filter(types=3)
    wine_card = whole_list.filter(types=4)
    salad = whole_list.filter(types=5)
    desserts = whole_list.filter(types=6)
    special = whole_list.filter(is_special=1)
    context ={'breakfast':breakfast,'lunch':lunch,'dinner':dinner,'desserts':desserts,'salad':salad,'winecard':wine_card,'special':special}
    return render(request, 'web/menu.html',context)

def recharge(request):
    member = Member.objects.get(id=request.session['webuser']['id'])
    money = float(member.money)
    if request.method == "POST":
        try:
            recharge = float(request.POST['recharge'])
            if recharge<0 or recharge > 100000:
                message = "充%.2f元?下次我一定放一个收款码在这里" %recharge
            else:
                money += recharge
                member.money = str(money)
                request.session['webuser'] = member.toDict()
                member.save()
                info = "充值成功！您当前余额为：" + str(money)
        except:
            message = "充值失败！您当前余额为：" + str(money)

    return render(request, 'web/recharge.html',locals())


# 产生验证码
def random_str():
    _str = '1QWERTT2YUIOP34LKJHG565FDSA567ZXCV890abcdWRGVGSfgh2123ijklmVBNMnopqrstu43vwxyz'
    return ''.join(random.choice(_str) for i in range(6))


def email_send(request):
    request.session.flush()
    info = '请您输入邮箱信息！'
    return render(request, 'web/email.html', locals())


def send_email(request):
    if request.method == 'GET':
        try:
            email = request.GET.get("email")
            print(email)
            if email.find("@") == -1 or not (email.endswith('.com') or email.endswith('.cn')):
                message = '请您检查邮箱输入是否正确！'
            elif not Member.objects.get(email=email):
                message = '该邮箱地址未注册!'
            else:
                email_code = random_str()
                msg = '您的验证码：%s \n晨曦实业欢迎您的光临！\n输入验证码请注意区分大小写哦！' %email_code
                send_mail('邮箱验证', msg, settings.DEFAULT_FROM_EMAIL, [email])
                request.session['email_code'] = email_code  # 将验证码保存到session中在接下来的操作中进行验证
                request.session['email'] = email
                info = '验证码发送成功，请注意查收！'
            return render(request, 'web/email.html',locals())
        except:
            # request.session['email'] = request.GET.get("email")
            message = '验证码发送失败！请检查您的邮箱！'
            return render(request, 'web/email.html',locals())
    else:
        # 验证验证码是否输入正确
        if request.POST['email_code'] == request.session['email_code']:
            message = '您已成功通过验证码登录!'
            ob = Member.objects.get(email=request.POST['email'])
            request.session['webuser'] = ob.toDict()
            request.session['member_is_login'] = True
            return render(request, 'web/index.html', locals())
        else:
            message = '验证码错误！'
            return render(request, 'web/email.html',locals())


