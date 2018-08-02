# 自定义中间件类
import re


from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.http import Http404
from django.utils import timezone

from .models import RobotKiller


class ShopMiddleware(object):
    """
    在线商城的中间件，控制登录页面的访问权限
    """
    max_visits = 10
    min_seconds = 600
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization(一次性配置和初始化).
        #print("ShopMiddleware")

    def __call__(self, request):
        # 通过 user_agent过滤爬虫
        http_user_agent = request.META.get('HTTP_USER_AGENT')
        http_user_agent = str(http_user_agent).lower()

        if "py" in http_user_agent or "ssl" in http_user_agent:
            raise Http404('你访问的页面不存在')

        # 通过IP限制频繁访问
        if not self.filter_ip(request):
            raise Http404('你访问的页面不存在')

        # 定义网站后台不用登录也可访问的路由url
        urllist = ['/myadmin/login', '/myadmin/dologin', '/myadmin/logout', '/myadmin/verify']
        # 获取当前请求路径
        path = request.path
        #print("Hello World!"+path)
        # 判断当前请求是否是访问网站后台,并且path不在urllist中
        if re.match("/myadmin", path) and (path not in urllist):
            # 判断当前用户是否没有登录
            if "adminuser" not in request.session:
                # 执行登录界面跳转
                return redirect(reverse('myadmin_login'))

        if re.match("^/orders", path) or re.match('^/vip', path):
            if 'vipuser' not in request.session:
                return redirect(reverse('login'))

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        return response

    def filter_ip(self, request):
        """
        反扒
        """
        domain = request.META.get('REMOTE_HOST')
        white_list = ['googlebot.com', 'crawl.baidu.com', 'sogou.com', 'bing.com', 'yahoo.com']
        for bot_domain in white_list:
            if domain.find(bot_domain) > 0:
                return True

        user_ip = request.META['REMOTE_ADDR']

        try:
            record = RobotKiller.objects.get(ip=user_ip)
        except RobotKiller.DoesNotExist:
            RobotKiller.objects.create(
                ip=user_ip, visits=1, time=timezone.now()
            )
            return True

        passed_seconds = (timezone.now() - record.time).seconds

        if record.visits > self.max_visits and passed_seconds < self.min_seconds:
            print('爬虫的不要.....')
            return False
        else:
            if passed_seconds < self.min_seconds:
                record.visits = record.visits + 1
                record.save()
            else:
                record.visits = 1
                record.time = timezone.now()
                record.save()
            return True
