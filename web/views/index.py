from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse

from common.models import Member

# Create your views here.
def index(request):
    """
    商城前台首页
    """
    # return HttpResponse("欢迎来到在线商城首页")
    return render(request, 'web/index.html')

def good_list(request, pindex=1):
    """
    商品列表
    """
    return render(request, 'web/list.html')

def good_detail(request, gid):
    """
    商品详情页
    """
    return render(request, 'web/detail.html')

def login(request):
    """
    加载登录页面
    """
    return render(request, 'web/login.html')

def dologin(request):
    """
    执行登录
    """
    print('执行登录...')
    code = request.POST['code']
    if request.session['verifycode'] != code:
        context = {'info': '验证码错误！'}
        return render(request, "web/login.html", context)

    try:
        #根据账号获取登录者信息
        user = Member.objects.get(nick_name=request.POST['username'])
        #判断当前用户是否是后台管理员用户
        if user.state == 0 or user.state == 1:
            # 验证密码
            import hashlib
            m = hashlib.md5()
            m.update(bytes(request.POST['password'], encoding="utf8"))
            if user.password == m.hexdigest():
                # 此处登录成功，将当前登录信息放入到session中，并跳转页面
                request.session['vipuser'] = user.toDict()
                return redirect(reverse('index'))
            else:
                context = {'info': '登录密码错误！'}
        else:
            context = {'info': '此用户为非法用户！'}
    except:
        context = {'info': '登录账号错误！'}

    print(context)
    return render(request, "web/login.html", context)

def logout(request):
    """
    退出登录
    """
    del request.session['vipuser']
    # 跳转登录页面（url地址改变）
    return redirect(reverse('login'))
