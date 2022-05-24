from django import forms
from captcha.fields import CaptchaField

class UserForm(forms.Form):
    # 表单，方便html部分快速输入
    name = forms.CharField(label="登录账号:", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "UserName"}))
    password = forms.CharField(label="输入密码:", max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control', "placeholder": "Password"}))
    captcha = CaptchaField(label='验证码:')

class MemberForm(forms.Form):
    # 表单，方便html部分快速输入
    # nickname = forms.CharField(label="昵称:", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "您的昵称"}))
    # name = forms.CharField(label="登录账号:", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "登录账号"}))
    # mobile = forms.CharField(label="联系电话:", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "请输入您的联系号码"}))
    # address = forms.CharField(label="常用地址:", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "您的常用地址"}))
    # password = forms.CharField(label="输入密码:", max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control', "placeholder": "请输入8-20位密码"}))
    # password2 = forms.CharField(label="确认密码:", max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control', "placeholder": "请确认输入密码"}))
    # email = forms.EmailField(label="邮箱地址:",
    #                          widget=forms.EmailInput(attrs={'class': 'form-control', "placeholder": "请正确输入邮箱"}))
    captcha = CaptchaField(label='验证码:')