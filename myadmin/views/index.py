from datetime import datetime

from django.core.mail import send_mail
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from myadmin.models import User, Member, Orders
from myadmin.form import UserForm

def index(request):
    today = datetime.now().date()
    orders = Orders.objects.filter(update_at__gt=today)
    today_count = orders.count()
    request.session['today_count'] = today_count
    get_orders = orders.filter(payment_status=2)
    income_today = 0
    for vo in get_orders:
        income_today += vo.whole_price
    request.session['income_today'] = '%.2f' %income_today
    member = Member.objects.filter(create_at__gt=today)
    vip_member = member.filter(is_vip=1)
    today_member = member.count()
    today_vip_member = vip_member.count()
    request.session['today_member'] = today_member
    request.session['today_vip_member'] = today_vip_member
    return render(request,"myadmin/index/index.html",locals())

def login(request):
    login_form = UserForm()
    return render(request, 'myadmin/index/tologin.html', locals())

def dologin(request):
    info = ""
    if request.session.get('is_login', None):  # 已经登录，跳转主页
        return redirect(reverse('myadmin_index'))
    if request.method == "POST":
        login_form = UserForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['name']
            password = login_form.cleaned_data['password']
            try:
                # 根据登录账号获取用户信息
                user = User.objects.get(username=username)
                # 校验当前用户状态是否是管理员
                if user.status == 6:
                    # 获取密码并md5
                    import hashlib
                    md5 = hashlib.md5()
                    n = user.password_salt
                    s = password + str(n)
                    md5.update(s.encode('utf-8'))
                    if user.password_hash == md5.hexdigest():
                        request.session['adminuser'] = user.toDict() # 登录成功后信息存入session
                        request.session['is_login'] = True
                        return redirect(reverse('myadmin_index'))
                    else:
                        info = "登录密码错误！"
                else:
                    info = "账号错误或非后台管理账号！"
            except Exception as err:
                print(err)
                info = "登录账号不存在！"
        else:
            info = "请您认真填写内容！"
    print(info)
    login_form = UserForm()
    return render(request, "myadmin/index/tologin.html", locals())


def logout(request):
    """执行退出"""
    del request.session['adminuser']
    request.session['is_login'] = False
    return redirect("/myadmin_login/")
