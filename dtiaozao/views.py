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

class Userform(ModelForm):
    class Meta:
        model = User
        fields = ["student_id","passwd","name","avatar","signature","phone","email"]

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

#个人中心
def self(req):
    if not req.session.get('islogin'):
        msg = '你还未登陆，请先登陆！'
        return render(req, 'error_msg.html', locals())
    if req.method == 'GET':
        uid = req.session['user_info']['uid']
        self_infos = User.objects.filter(uid=uid)
        return render(req,'user/self.html',locals())
    # 修改个人信息
    uid = req.session['user_info']['uid']
    obj = User.objects.get(uid=uid)
    form = Userform(data = req.POST, files = req.FILES, instance = obj)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/self')
    msg = '表单格式有误'
    return render(req, 'error_msg.html', locals())

    
    