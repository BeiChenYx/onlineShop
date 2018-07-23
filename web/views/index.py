from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    """
    商城前台首页
    """
    # return HttpResponse("欢迎来到在线商城首页")
    return render(request, 'web/index.html')

def good_list(request):
    """
    商品列表
    """
    pass

def good_detail(request):
    """
    商品详情页
    """
    pass
