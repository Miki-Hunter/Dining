import hashlib
import os
import random
import time
from datetime import datetime
from django.shortcuts import render
from django.shortcuts import redirect
from Dining.settings import PROJECT_ROOT
from myadmin.form import UserForm, MemberForm
from myadmin.models import User, Shop, Category, Product, Member


def register(request):
    if request.session.get('member_is_login', None):
        # 登录状态不允许注册
        return redirect("/index_index/")
    if request.method == "POST":
        try:
            email = request.POST['email']
            same_name_user = Member.objects.filter(name=request.POST['membername'])
            same_email_user = Member.objects.filter(email=email)
            myfile = request.FILES.get("avatar", None)
            if len(request.POST['membername']) > 9:
                message = "您的昵称太长！"
            elif len(request.POST['password1']) < 8 or len(request.POST['password1']) > 20:
                message = "请输入8~20位密码哦！"
            elif request.POST['password1'] != request.POST['password2']:
                message = "两次输入的密码不同！"
            elif same_name_user:  # 用户名唯一
                message = '用户已经存在，请重新选择用户名！'
            elif email.find("@") == -1 or not (email.endswith('.com') or email.endswith('.cn')):
                message = '请您检查邮箱输入是否正确！'
            elif same_email_user:  # 邮箱地址唯一
                message = '该邮箱地址已被注册，请使用其他邮箱！'
            else:
                if not myfile:
                    cover_pic = 'model.jpg' # 此为默认头像
                else:
                    cover_pic = str(time.time()) + "." + myfile.name.split('.').pop()
                    destination = open(PROJECT_ROOT + "/static/uploads/member/" + cover_pic, "wb")
                    for chunk in myfile.chunks():  # 分块写入文件
                        destination.write(chunk)
                    destination.close()
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
                info = '注册成功！'
                login_form = UserForm()
                return render(request, 'web/login.html', locals())
        except Exception as err:
            print(err)
            message = '注册失败！'
    register_form = MemberForm()
    return render(request, 'web/register.html', locals())

def login(request):
    """加载登录页面"""
    login_form = UserForm()
    return render(request, 'web/login.html', locals())

def dologin(request):
    """执行登录"""
    message = ""
    if request.session.get('member_is_login', None):  # 已经登录，跳转主页
        return render(request, 'web/index.html')
    if request.method == "POST":
        # 根据登录账号获取用户信息
        login_form = UserForm(request.POST)
        if login_form.is_valid():
            name = login_form.cleaned_data['name']
            password = login_form.cleaned_data['password']
            try:
                user = Member.objects.get(name=name)  # 校验当前用户是否存在
                import hashlib
                md5 = hashlib.md5()
                n = user.password_salt
                s = password + str(n)
                md5.update(s.encode('utf-8'))
                if user.password_hash == md5.hexdigest():
                    request.session['webuser'] = user.toDict()
                    request.session['member_is_login'] = True
                    message = "登录成功!"
                    return render(request, 'web/index.html', locals())  # 跳转首页
                else:
                    message = "密码输入错误！"
            except:
                message = "登录账号不存在！"
                print(message)
        else:
            message = "请您认真填写内容！"
    login_form = UserForm()
    return render(request, 'web/login.html', locals())

def edit(request, mid):
    if request.method == "POST":
        try:
            ob = Member.objects.get(id=mid)
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
            ob.email = request.POST['email']
            ob.introduce = request.POST['introduce']
            ob.avatar = avatar
            ob.update_at = datetime.now()
            request.session['webuser'] = ob.toDict()
            ob.save()
            message = '修改成功！'
        except Exception as err:
            print(err)
            info = '修改失败！'
        return render(request, 'web/index.html', locals())
    else:
        ob = Member.objects.get(id=mid)
        context = {"member": ob}
        return render(request, "web/edit.html", context)

def logout(request):
    """执行退出"""
    # request.session.flush()  # 删除当前的会话数据和会话cookie。经常用在用户退出后，删除会话
    del request.session['webuser']
    del request.session['email_code']
    del request.session['email']
    request.session['member_is_login'] = False
    message = "成功退出登录!"
    return render(request, 'web/index.html', locals())  # 跳转首页