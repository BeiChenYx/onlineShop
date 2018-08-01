"""onlineShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from .views import index, cart, orders

urlpatterns = [
    url(r'^$', index.index, name='index'),
    url(r'^list$', index.good_list, name='good_list'),
    url(r'^list/(?P<pindex>[0-9]+)$', index.good_list, name='good_list'),
    url(r'^detail/(?P<gid>[0-9]+)$', index.good_detail, name='good_detail'),

    # 会员登录路由管理
    url(r'^login$', index.login, name='login'),
    url(r'^dologin$', index.dologin, name='dologin'),
    url(r'^logout$', index.logout, name='logout'),

    # 购物车路由器管理
    url(r'^cart$', cart.index, name='cart_index'), #浏览购物车
    url(r'^cart/add/(?P<gid>[0-9]+)$', cart.add, name='cart_add'), #添加购物车
    url(r'^cart/del/(?P<gid>[0-9]+)$', cart.delete, name='cart_del'), #从购物车中删除一个商品
    url(r'^cart/clear$', cart.clear, name='cart_clear'), #清空购物车
    url(r'^cart/change$', cart.change, name='cart_change'), #更改购物车中商品数量

    # 订单处理
    url(r'^orders/add$', orders.add, name='orders_add'), #订单的表单页
    url(r'^orders/confirm$', orders.confirm, name='orders_confirm'), #订单确认页
    url(r'^orders/insert$', orders.insert, name='orders_insert'), #执行订单添加操作
]
