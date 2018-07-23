import io
import hashlib
import random
from PIL import Image, ImageDraw, ImageFont

from django.shortcuts import render
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse

from common.models import Member

# Create your views here.
def index(request):
    """
    加载主页
    """
    return render(request, 'myadmin/index.html')

def login(request):
    """
    会员登录页面
    """
    return render(request, 'myadmin/login.html')

def dologin(request):
    """
    执行会员登录
    """
    try:
        user_name = request.POST['name']
        password = request.POST['password']
        code = request.POST['code']
        if request.session['verifycode'] != code:
            context = {'info': '验证码错误！'}
            return render(request, "myadmin/login.html", context)

        user = Member.objects.get(nick_name=user_name)
        if user.state == 0:
            password_md5 = hashlib.md5()
            password_md5.update(bytes(password, encoding='utf-8'))
            if password_md5.hexdigest() == user.password:
                request.session['adminuser'] = user.user_name
                return redirect(reverse('myadmin_index'))
            else:
                context = {'info': '密码错误'}
        else:
            context = {'info': '账户不是管理员'}
    except Exception as err:
        context = {'info': '登录账号错误: %s' % str(err)}
    return render(request, 'myadmin/info.html', context)

def logout(request):
    """
    会员退出
    """
    del request.session['adminuser']
    return redirect(reverse('myadmin_login'))

def verify(request):
    """
    验证码
    """
    #定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(20, 100), 100)
    # bgcolor = (242, 164, 247)
    width = 100
    height = 35
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    #构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('static/msyh.ttc', 21)
    #font = ImageFont.load_default().font
    #构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    # 内存文件操作-->此方法为python3的
    buf = io.BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')
