import hashlib
from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator

from common.models import Member


def index(request, pindex=1):
    """
    浏览会员信息
    """
    member_data = Member.objects
    mywhere = list()
    kw = request.GET.get('keyword', None)
    if kw:
        member_nead = member_data.filter(
            Q(user_name__contains=kw) | Q(nick_name__contains=kw)
        )
        mywhere.append('keyword=' + kw)
    else:
        member_nead = member_data.filter()

    sex = request.GET.get('sex', '')
    if sex != '':
        member_nead = member_nead.filter(sex=sex)
        mywhere.append('sex=' + sex)

    pIndex = int(pindex)
    page = Paginator(member_nead, 2)
    maxpages = page.num_pages
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1

    member_nead = page.page(pIndex)
    page_no = page.page_range
    context = {
        'userslist': member_nead,
        'plist': page_no,
        'pIndex': pIndex,
        'maxpages': maxpages,
        'mywhere': mywhere,
    }

    return render(request, 'myadmin/users/index.html', context)

def add(request):
    """
    加载添加会员页面
    """
    return render(request, 'myadmin/users/add.html')

def insert(request):
    """
    执行添加会员页面
    """
    try:
        user_info = Member()
        user_info.user_name = request.POST['user_name']
        user_info.nick_name = request.POST['nick_name']
        password = hashlib.md5()
        password.update(bytes(request.POST['password'], encoding="utf8"))
        user_info.password = password.hexdigest()
        user_info.sex = request.POST['sex']
        user_info.address = request.POST['address']
        user_info.code = request.POST['code']
        user_info.phone = request.POST['phone']
        user_info.email = request.POST['email']
        user_info.save()
        context = {'info': '会员信息添加成功'}
    except Exception as err:
        context = {'info': '会员信息添加失败: %s' % str(err)}
    return render(request, 'myadmin/info.html', context)

def delete(request, uid):
    """
    删除会员信息
    """
    try:
        user = Member.objects.filter(id=uid)
        user.delete()
        context = {'info': '会员信息删除成功'}
    except Exception as err:
        context = {'info': '会员信息删除失败: %s' % str(err)}
    return render(request, 'myadmin/info.html', context)

def edit(request, uid):
    """
    加载修改会员信息页面
    """
    try:
        user = Member.objects.get(id=uid)
        print('user: ', user)
        return render(request, 'myadmin/users/edit.html', {'user': user})
    except Exception as err:
        context = {'info': '会员信息添加失败: %s' % str(err)}
        print(context)
        return render(request, 'myadmin/info.html', context)

def update(request, uid):
    """
    执行修改会员信息
    """
    try:
        user_info = Member.objects.get(id=uid)
        user_info.user_name = request.POST['user_name']
        user_info.nick_name = request.POST['nick_name']
        password = hashlib.md5()
        password.update(bytes(request.POST['password'], encoding="utf8"))
        user_info.password = password.hexdigest()
        user_info.sex = request.POST['sex']
        user_info.address = request.POST['address']
        user_info.code = request.POST['code']
        user_info.phone = request.POST['phone']
        user_info.email = request.POST['email']
        user_info.save()
        context = {'info': '会员信息修改成功'}
    except Exception as err:
        context = {'info': '会员信息修改失败: %s' % str(err)}
    return render(request, 'myadmin/info.html', context)

def reset_pass(request, uid):
    """
    重置用户密码, 系统管理员用户才可以修改
    """
    try:
        user = Member.objects.get(id=uid)
        return render(request, 'myadmin/users/reset.html', {'user': user})
    except Exception as err:
        context = {'info': '会员密码重置失败: %s' % str(err)}
        print(str(err))
        return render(request, 'myadmin/info.html', context)

def doreset_pass(request, uid):
    """
    执行用户密码的修改
    """
    try:
        user_info = Member.objects.get(id=uid)
        password = hashlib.md5()
        password.update(bytes(request.POST['password'], encoding="utf8"))
        user_info.password = password.hexdigest()
        user_info.save()
        context = {'info': '会员密码重置成功'}
    except Exception as err:
        context = {'info': '会员密码重置失败 %s' % str(err)}
    return render(request, 'myadmin/info.html', context)
