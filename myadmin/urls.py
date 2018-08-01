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
from .views import index, users, category, goods, orders

urlpatterns = [
    # 后台首页
    url(r'^$', index.index, name='myadmin_index'),

    # 后台用户管理
    url(r'^users/(?P<pindex>[0-9]+)$', users.index, name="myadmin_users_index"),
    url(r'^users/add$', users.add, name="myadmin_users_add"),
    url(r'^users/insert$', users.insert, name="myadmin_users_insert"),
    url(r'^users/del/(?P<uid>[0-9]+)$', users.delete, name="myadmin_users_del"),
    url(r'^users/edit/(?P<uid>[0-9]+)$', users.edit, name="myadmin_users_edit"),
    url(r'^users/update/(?P<uid>[0-9]+)$', users.update, name="myadmin_users_update"),
    url(r'^users/reset/(?P<uid>[0-9]+)$', users.reset_pass, name="myadmin_users_reset"),
    url(r'^users/doreset/(?P<uid>[0-9]+)$', users.doreset_pass, name="myadmin_users_doreset"),

    # 后台管理员路由
    url(r'^login$', index.login, name="myadmin_login"),
    url(r'^dologin$', index.dologin, name="myadmin_dologin"),
    url(r'^logout$', index.logout, name="myadmin_logout"),
    url(r'^verify$', index.verify, name="myadmin_verify"),

    # 后台商品类别信息管理
    url(r'^category$', category.index, name="myadmin_category_index"),
    url(r'^category/add/(?P<tid>[0-9]+)$', category.add, name="myadmin_category_add"),
    url(r'^category/insert$', category.insert, name="myadmin_category_insert"),
    url(r'^category/del/(?P<tid>[0-9]+)$', category.delete, name="myadmin_category_del"),
    url(r'^category/edit/(?P<tid>[0-9]+)$', category.edit, name="myadmin_category_edit"),
    url(r'^category/update/(?P<tid>[0-9]+)$', category.update, name="myadmin_category_update"),

    # 商品信息管理
    url(r'^goods$', goods.index, name="myadmin_goods_index"),
    url(r'^goods/add$', goods.add, name="myadmin_goods_add"),
    url(r'^goods/insert$', goods.insert, name="myadmin_goods_insert"),
    url(r'^goods/del/(?P<gid>[0-9]+)$', goods.delete, name="myadmin_goods_del"),
    url(r'^goods/edit/(?P<gid>[0-9]+)$', goods.edit, name="myadmin_goods_edit"),
    url(r'^goods/update/(?P<gid>[0-9]+)$', goods.update, name="myadmin_goods_update"),

    # 订单管理
    url(r'^orders$', orders.index, name="myadmin_orders_index"),
    url(r'^orders/(?P<pIndex>[0-9]+)$', orders.index, name="myadmin_orders_index"),
    url(r'^orders/detail/(?P<oid>[0-9]+)$', orders.detail, name="myadmin_orders_detail"),
    url(r'^orders/state$', orders.state, name="myadmin_orders_state"),
]
