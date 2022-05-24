from django.contrib import admin
from django.urls import include,path

urlpatterns = [
    path('', include("web.urls")),                # 前台大堂点餐端
    path('myadmin/', include("myadmin.urls")),     # 后台管理端
    path('mobile/', include("mobile.urls")),    # 移动会员端
    path('captcha', include('captcha.urls')),
]