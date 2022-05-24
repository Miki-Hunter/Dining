from datetime import datetime

from django.core.paginator import Paginator
from django.shortcuts import render

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

# def sendMessage(email):  # 发送邮件并返回验证码
#     # 生成验证码
#     import random
#     str1 = '01234567897823412343204726371673zqscfwfwjxixqiqoeywrtezxzncvvzqvdwobxsu'
#     rand_str = ''
#     for i in range(0, 6):
#         rand_str += str1[random.randrange(0, len(str1))]
#     # 发送邮件：
#     # send_mail的参数分别是  邮件标题，邮件内容，发件箱(settings.py中设置过的那个)，收件箱列表(可以发送给多个人),失败静默(若发送失败，报错提示我们)
#     message = "您的验证码是" + rand_str + "，10分钟内有效，请尽快填写"
#     emailBox = []
#     emailBox.append(email)
#     send_mail('怪奇物语', message, 'mikihunter11235@gmail.com', emailBox, fail_silently=False)
#     return rand_str
#
#
# # 验证该用户是否已存在 created = 1 存在
# def existUser(email):
#     created = 1
#     try:
#         Member.objects.get(email=email)
#     except:
#         created = 0
#     return created
#
#
def reg(request):
    pass
#     if request.POST.get('type') == 'sendMessage':
#         print(request.POST.get('email'))
#         email = request.POST.get('email')
#         response = {"state": False, "errmsg": ""}
#
#         if existUser(email):
#             response['errmsg'] = '该用户已存在，请登录'
#         else:
#             try:
#                 rand_str = sendMessage(email)  # 发送邮件
#                 request.session['verify'] = rand_str  # 验证码存入session，用于做注册验证
#                 response['state'] = True
#             except:
#                 response['errmsg'] = '验证码发送失败，请检查邮箱地址'
#         return HttpResponse(json.dumps(response))
#     else:
#         return render(request, 'web/email.html', locals())  # 跳转首页
