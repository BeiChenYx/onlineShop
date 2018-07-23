import hashlib

from django.shortcuts import render

from common.models import Category


def index(request):
    """
    浏览商品类别信息
    """
    # 执行数据查询，并放置到模板中
    # category_list = Category.objects.extra(select={'_has': 'concat(path,id)'}).order_by('_has')
    # 上面的concat的方法在sqllite中不存在，所以使用python来处理
    categorys = Category.objects.all()
    # 遍历查询结果，为每个结果对象追加一个pname属性，目的用于缩进标题
    for category in categorys:
        category.pname = '. . . '*(category.path.count(',') - 1)
        category.path_id = category.path + str(category.id)
    categorys_list = list(categorys)
    categorys_list.sort(key=lambda elem: elem.path_id)
    context = {"typeslist": categorys_list}
    return render(request, 'myadmin/category/index.html', context)

def add(request, tid):
    """
    加载添加商品类别页面
    """
    # 获取父类别信息，若没有则默认为根类别信息
    if tid == '0':
        context = {'pid': 0, 'path': '0,', 'name': '根类别'}
    else:
        ob = Category.objects.get(id=tid)
        context = {'pid': ob.id, 'path': ob.path+str(ob.id)+',', 'name': ob.name}
    return render(request, 'myadmin/category/add.html', context)

def insert(request):
    """
    执行添加商品类别页面
    """
    try:
        category_info = Category()
        category_info.name = request.POST['name']
        category_info.pid = request.POST['pid']
        category_info.path = request.POST['path']
        category_info.save()
        context = {'info': '会员信息添加成功'}
    except Exception as err:
        context = {'info': '会员信息添加失败: %s' % str(err)}
    return render(request, 'myadmin/info.html', context)

def delete(request, tid):
    """
    删除商品类别信息
    """
    # 获取被删除商品的子类别信息量，若有数据，就禁止删除当前类别
    try:
        row = Category.objects.filter(pid=tid).count()
        if row > 0:
            context = {'info': '删除失败：此类别下还有子类别！'}
            return render(request, "myadmin/info.html", context)
        category = Category.objects.filter(id=tid)
        category.delete()
        context = {'info': '商品类别信息删除成功'}
    except Exception as err:
        context = {'info': '商品类别信息删除失败: %s' % str(err)}
    return render(request, 'myadmin/info.html', context)

def edit(request, tid):
    """
    加载修改商品类别信息页面
    """
    try:
        ob = Category.objects.get(id=tid)
        context = {'type': ob}
        return render(request, "myadmin/category/edit.html", context)
    except Exception as err:
        context = {'info': '没有找到要修改的信息:%s' % str(err)}
    return render(request, "myadmin/info.html", context)

def update(request, tid):
    """
    执行修改商品类别信息
    """
    try:
        ob = Category.objects.get(id=tid)
        ob.name = request.POST['name']
        ob.save()
        context = {'info': '修改成功！'}
    except Exception as err:
        print(err)
        context = {'info': '修改失败！'}
    return render(request, "myadmin/info.html", context)
