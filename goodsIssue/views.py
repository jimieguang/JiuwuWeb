#encoding: utf-8
from django import forms
from django.forms import ModelForm
from django.shortcuts import render,HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext

from userIssue.models import User
from goodsIssue.models import Goodsissue, MessageCompose, MessageComment
from dtiaozao import function as fun

class Goodsform(ModelForm):
    class Meta:
        model = Goodsissue
        fields = ["name","price","buy_price","introduction","imagefile"]
    def clean_issuedate(self):
        '''钩子函数：更新商品时间'''
        return fun.now()
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder" : field.label}
            # 禁用表单编辑
            # field.disabled = True

def newGoods(req):
    '''发布新的商品'''
    if req.method == 'GET':
        return render(req, 'goods/new_goods.html', locals())
    # 提取表单数据保存到数据库
    data = req.POST
    form = Goodsform(data=data)
    if form.is_valid():
        infos = form.cleaned_data
        #获取发布者ID
        uid = req.session['user_info']['uid']
        infos["owner_id"] = uid
        infos["issuedate"] = fun.now()
        infos["imagefile"] = fun.save_image(data["imagefile_name"],data["imagefile"])
        Goodsissue.objects.create(**infos)
        return HttpResponseRedirect("myGoods/all/")
    return render(req, 'goods/new_goods.html', locals())

def delGoods(req):
    '''删除特定商品(仅限本人）'''
    if req.method == 'GET':
        msg = "无效的请求路径"
        return render(req, 'error_msg.html', locals())
    data = req.POST
    goods_id = data.get('goods_id')
    goods = Goodsissue.objects.get(id=goods_id)
    if req.session['user_info']['uid'] == goods.owner.id:
        goods.imagefile.delete()
        goods.delete()                #仅调用delete无法删除imagefield文件
    return HttpResponse("删除成功")


    


def myGoods(req,during):
    '''展示我的商品'''
    if req.method == 'GET':
        start = fun.timeTrans(during)
        end = fun.now()
        uid = req.session['user_info']['uid']
        #获取用户名下所有商品信息(限制发布时间,并降序排列)
        goods_infos = Goodsissue.objects.filter(owner=uid,issuedate__range = [start,end]).order_by('-issuedate')
        goods_num = goods_infos.count()
        return render(req, 'goods/goods_list.html', locals())
    # 修改商品信息(待优化)
    data = req.POST
    id = req.GET['id']
    obj = Goodsissue.objects.get(id=id)
    form = Goodsform(data=data, files=req.FILES,instance = obj)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("goodsIssue/myGoods/all")
    msg = '表单格式有误'
    return render(req, 'error_msg.html', locals())


#商品浏览模块
def goodsList(req,during):
    if req.method == 'POST':
        msg = '非法访问！！！'
        return render(req,'error_msg.html', locals())
    start = fun.timeTrans(during)
    end = fun.now()
    # 获取指定时间段商品数据
    goods_infos = Goodsissue.objects.filter(issuedate__range = [start,end]).order_by('-issuedate')
    goods_num = goods_infos.count()
    return render(req, 'goods/goods_list.html', locals())


#商品详情页模块(增加留言功能)
def goodsDetail(req,goods_id):
    if req.method == 'GET':
        goods = Goodsissue.objects.get(id=goods_id)
        # 判断商品是否属于本人以决定赋予编辑权限与否
        try:
            isOwner = (goods.owner_id == req.session['user_info']['uid'])
        except KeyError:
            isOwner = False
        # 评论母表
        msg_ces = MessageCompose.objects.filter(goods=goods)
        msg_ces_num = msg_ces.count()
        msg_cts_list = []
        # 评论子表
        for i in range(msg_ces_num):
            msg_cts = MessageComment.objects.filter(reply_from=msg_ces[i])
            msg_cts_list.append(msg_cts)
        return render(req, 'goods/goods_detail.html', locals())
    # 响应留言操作(将留言保存在数据库)
    data = req.POST
    message_infos = {}
    message_infos["owner_id"] = req.session['user_info']['uid']
    message_infos["messagedate"] = fun.now()
    message_infos["content"] = data.get('content')
    if data.get('reply_from'):
        # 需要更改modelform，并且区别评论母子表，删除评论栏模块
        message_infos["reply_from_id"] = data.get('reply_from')
        if data.get('reply_from')!=data.get('reply_to'):
            message_infos["reply_to_id"] = data.get('reply_to')
        MessageComment.objects.create(**message_infos)
    else:
        message_infos["goods_id"] = goods_id
        MessageCompose.objects.create(**message_infos)
    return HttpResponseRedirect("./")
