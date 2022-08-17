#encoding: utf-8
__author__ = 'hadoop'

from re import L
from django.shortcuts import render
from django.template import RequestContext
from userIssue.models import User
from goodsIssue.models import Goodsissue, MessageCompose, MessageComment
from django.forms import ModelForm
from django.http import HttpResponseRedirect
# 自定义函数
from dtiaozao import function as fun


#主页
def index(req):
    isLogin = req.session.get('islogin')
    if isLogin == True:
        uid = req.session.get('user_info')["uid"]
        user = User.objects.get(id=uid)
        name = user.name
        avatar = user.avatar
        print(name)
    else:
        isLogin = False
    return render(req, 'index.html', locals())


#搜索引擎模块
def search(req,during):
    goods_name = req.GET.get('keywords')
    if goods_name==None:
        goods_name = ""
    start = fun.timeTrans(during)
    end = fun.now()
    # 获取指定时间段且具有该关键词的商品数据
    goods_infos = Goodsissue.objects.filter(issuedate__range = [start,end],name__contains=goods_name).order_by('-issuedate')
    goods_num = len(goods_infos)
    return render(req, 'goods/goods_list.html', locals())



    
    