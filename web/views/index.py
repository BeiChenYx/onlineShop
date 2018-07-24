from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse

from common.models import Member, Category, Goods

# Create your views here.
def load_top_category(request):
    """
    加载一级类别
    """
    categorys = Category.objects.filter(pid=0)
    return {'categorys': categorys}

def index(request):
    """
    商城前台首页
    """
    # return HttpResponse("欢迎来到在线商城首页")
    return render(request, 'web/index.html', load_top_category(request))

def good_list(request, pindex=1):
    """
    商品列表
    TODO: 后台做了分页处理，此处就不做分页处理，处理方式是一样的
    商品展示就直接一行4个，一直排下去
    """
    context = load_top_category(request)
    goods = Goods.objects.all()
    rows = len(goods) // 4 + (1 if len(goods) % 4 else 0)

    context['rows'] = tuple(range(0, rows))
    context['coles'] = (0, 1, 2, 3)
    # 构造二维列表
    context['goods'] = [goods[row*4: row*4+4] for row in range(0, rows)]
    return render(request, 'web/list.html', context)

def good_detail(request, gid):
    """
    商品详情页
    """
    return render(request, 'web/detail.html', load_top_category(request))

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
