"""
商品信息的视图
"""
import os
import time
from datetime import datetime


from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image

from common.models import Category, Goods


def index(request):
    """
    浏览商品信息
    """
    # 执行数据查询，并放置到模板中
    goods_list = Goods.objects.all()
    for ob in goods_list:
        ty = Category.objects.get(id=ob.typeid)
        ob.typename = ty.name
    context = {"goodslist": goods_list}
    return render(request, 'myadmin/goods/index.html', context)


def add(request):
    """
    商品信息添加表单
    """
    # 获取商品的类别信息
    categorys = Category.objects.all()
    # 遍历查询结果，为每个结果对象追加一个pname属性，目的用于缩进标题
    for category in categorys:
        category.path_id = category.path + str(category.id)
        print('category.pid: ', category.pid)
    categorys_list = list(categorys)
    categorys_list.sort(key=lambda elem: elem.path_id)
    context = {"typelist": categorys_list}
    return render(request, 'myadmin/goods/add.html', context)


def insert(request):
    """
    执行商品类别信息添加
    """
    try:
        # 判断并执行图片上传，缩放等处理
        myfile = request.FILES.get("pic", None)
        if not myfile:
            return HttpResponse("没有上传文件信息！")
        # 以时间戳命名一个新图片名称
        filename = str(time.time())+"."+myfile.name.split('.').pop()
        destination = open(os.path.join("./static/goods/", filename), 'wb+')
        for chunk in myfile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()

        # 执行图片缩放
        im = Image.open("./static/goods/"+filename)
        # 缩放到375*375:
        im.thumbnail((375, 375))
        # 把缩放后的图像用jpeg格式保存:
        im.save("./static/goods/"+filename, 'jpeg')
        # 缩放到220*220:
        im.thumbnail((220, 220))
        # 把缩放后的图像用jpeg格式保存:
        im.save("./static/goods/m_"+filename, 'jpeg')
        # 缩放到75*75:
        im.thumbnail((75, 75))
        # 把缩放后的图像用jpeg格式保存:
        im.save("./static/goods/s_"+filename, 'jpeg')

        # 获取商品信息并执行添加
        ob = Goods()
        ob.goods = request.POST['goods']
        ob.typeid = request.POST['typeid']
        ob.company = request.POST['company']
        ob.price = request.POST['price']
        ob.store = request.POST['store']
        ob.content = request.POST['content']
        ob.picname = filename
        ob.state = 1
        ob.addtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': '添加成功！'}
    except Exception as err:
        print(err)
        context = {'info': '添加失败！'}
    return render(request, "myadmin/info.html", context)


def delete(request, gid):
    """
    执行商品信息删除
    """
    try:
        # 获取被删除商品信的息量，先删除对应的图片
        ob = Goods.objects.get(id=gid)
        #执行图片删除
        os.remove("./static/goods/"+ob.picname)
        os.remove("./static/goods/m_"+ob.picname)
        os.remove("./static/goods/s_"+ob.picname)
        #执行商品信息的删除
        ob.delete()
        context = {'info': '删除成功！'}
    except Exception as err:
        print(err)
        context = {'info': '删除失败！'}
    return render(request, "myadmin/info.html", context)


def edit(request, gid):
    """
    打开商品类别信息编辑表单
    """
    try:
        # 获取要编辑的信息
        ob = Goods.objects.get(id=gid)
        # 获取商品的类别信息
        # list = Category.objects.extra(select={'_has': 'concat(path,id)'}).order_by('_has')

        categorys = Category.objects.all()
        # 遍历查询结果，为每个结果对象追加一个pname属性，目的用于缩进标题
        for category in categorys:
            category.path_id = category.path + str(category.id)
            print('category.pid: ', category.pid)
        categorys_list = list(categorys)
        categorys_list.sort(key=lambda elem: elem.path_id)

        # 放置信息加载模板
        context = {"typelist": categorys_list, 'goods': ob}
        return render(request, "myadmin/goods/edit.html", context)
    except Exception as err:
        context = {'info': '没有找到要修改的信息: %s' % str(err)}
    return render(request, "myadmin/info.html", context)


def update(request, gid):
    """
    执行商品类别信息编辑
    """
    try:
        b = False
        oldpicname = request.POST['oldpicname']
        if None != request.FILES.get("pic"):
            myfile = request.FILES.get("pic", None)
            if not myfile:
                return HttpResponse("没有上传文件信息！")
            # 以时间戳命名一个新图片名称
            filename = str(time.time())+"."+myfile.name.split('.').pop()
            destination = open(os.path.join("./static/goods/", filename), 'wb+')
            for chunk in myfile.chunks():  # 分块写入文件
                destination.write(chunk)
            destination.close()
            # 执行图片缩放
            im = Image.open("./static/goods/"+filename)
            # 缩放到375*375:
            im.thumbnail((375, 375))
            # 把缩放后的图像用jpeg格式保存:
            im.save("./static/goods/"+filename, 'jpeg')
            # 缩放到220*220:
            im.thumbnail((220, 220))
            # 把缩放后的图像用jpeg格式保存:
            im.save("./static/goods/m_"+filename, 'jpeg')
            # 缩放到75*75:
            im.thumbnail((75, 75))
            # 把缩放后的图像用jpeg格式保存:
            im.save("./static/goods/s_"+filename, 'jpeg')
            b = True
            picname = filename
        else:
            picname = oldpicname
            ob = Goods.objects.get(id=gid)
            ob.goods = request.POST['goods']
            ob.typeid = request.POST['typeid']
            ob.company = request.POST['company']
            ob.price = request.POST['price']
            ob.store = request.POST['store']
            ob.content = request.POST['content']
            ob.picname = picname
            ob.state = request.POST['state']
            ob.save()
            context = {'info': '修改成功！'}
            if b:
                os.remove("./static/goods/m_"+oldpicname)  # 执行老图片删除
                os.remove("./static/goods/s_"+oldpicname)  # 执行老图片删除
                os.remove("./static/goods/"+oldpicname)  # 执行老图片删除
    except Exception as err:
        print(err)
        context = {'info': '修改失败！'}
        if b:
            os.remove("./static/goods/m_"+picname)  # 执行新图片删除
            os.remove("./static/goods/s_"+picname)  # 执行新图片删除
            os.remove("./static/goods/"+picname)  # 执行新图片删除
    return render(request, "myadmin/info.html", context)
