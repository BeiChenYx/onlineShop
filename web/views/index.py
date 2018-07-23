# from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    """
    商城前台首页
    """
    return HttpResponse("欢迎来到在线商城首页")
