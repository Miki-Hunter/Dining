from django.urls import path, include
from django.conf.urls import url, include
from web.views import index,cart,orders,login

urlpatterns = [
    # 前台大堂点餐首页
    path('', index.index, name="index_index"),

    # 用户登录注册
    path('login', login.login, name="web_login"),
    path('dologin', login.dologin, name="web_dologin"),
    path('register', login.register, name="web_register"),
    path('logout', login.logout, name="web_logout"),
    path('edit/<int:mid>', login.edit, name="web_edit"),
    path('reg', index.reg,name="web_email"),
    path('recharge', index.recharge,name="web_recharge"),

    path('open_web/',include([
        # 菜单
        path('menu/', index.menu, name="web_menu"),

        # 购物车信息管理路由配置

        path('cart/index', cart.index, name="cart_index"), #购物车首页
        path('cart/add/<str:pid>', cart.add, name="web_cart_add"), #购物车添加
        path('cart/adda/<str:pid>', cart.add_to_cart, name="cart_add"), #从菜单开始加入购物车
        path('cart/decrease/<str:pid>', cart.decrease, name="web_cart_decrease"), #购物车减少
        path('cart/del/<str:pid>', cart.delete, name="web_cart_del"),#购物车删除
        path('cart/clear', cart.clear, name="web_cart_clear"), #购物车清空
        # path('cart/change', cart.change, name="web_cart_change"),#购物车更改

        # 订单处理
        path('orders/<int:pIndex>', orders.index, name="web_orders_index"), #浏览订单
        path('orders/insert', orders.insert, name='web_orders_insert'),  # 执行订单添加操作
        path('orders/detail', orders.detail,name='web_orders_detail'), #订单的详情信息
        path('orders/status', orders.status,name='web_orders_status'), #修改订单状态

    ]))
]