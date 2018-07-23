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
from .views import index

urlpatterns = [
    url(r'^$', index.index, name='index'),
    url(r'^list$', index.good_list, name='good_list'),
    url(r'^detail/(?P<gid>[0-9]+)$', index.good_detail, name='good_detail'),

    # 会员登录路由管理
    url(r'^login$', index.login, name='login'),
    url(r'^dologin$', index.dologin, name='dologin'),
    url(r'^logout$', index.logout, name='logout'),
]
