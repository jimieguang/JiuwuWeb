#encoding: utf-8
from django import forms
from django.forms import ModelForm
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import RequestContext

from . import controller
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
    if not req.session.get('islogin'):
        msg = '你还未登陆，请先登陆！'
        return render(req, 'error_msg.html', locals())
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
        return HttpResponseRedirect("myGoods")


def myGoods(req):
    '''展示我的商品'''
    if not req.session.get('islogin'):
        msg = '你还未登陆，请先登陆！'
        return render(req, 'error_msg.html', locals())
    if req.method == 'GET':
        uid = req.session['user_info']['uid']
        #获取用户名下所有商品信息
        goods_infos = Goodsissue.objects.filter(owner=uid)
        goods_num = len(goods_infos)
        return render(req, 'goods/goods_list.html', locals())
    # 修改商品信息
    data = req.POST
    id = req.GET['id']
    obj = Goodsissue.objects.get(id=id)
    form = Goodsform(data=data, files=req.FILES,instance = obj)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("goodsIssue/myGoods")
    msg = '表单格式有误'
    return render(req, 'error_msg.html', locals())


#商品下架模块
def delGoods(req):
    data = req.GET
    isDel = controller.del_goods(data)
    if isDel == -1:
        msg = '删除商品失败，请联系管理员！'
        return render(req, 'error_msg.html', locals())
    uid = req.session['user_info']['uid']
    rt = controller.get_goods(uid)
    return HttpResponseRedirect('issue')

#商品浏览模块
def goodsList(req,during):
    if req.method == 'POST':
        msg = '非法访问！！！'
        return render(req,'error_msg.html', locals())
    start = fun.timeTrans(during)
    end = fun.now()
    # 获取指定时间段商品数据
    goods_infos = Goodsissue.objects.filter(issuedate__range = [start,end])
    goods_num = len(goods_infos)
    return render(req, 'goods/goods_list.html', locals())


#商品详情页模块(增加留言功能)
def goodsDetail(req,goods_id):
    if not req.session.get('islogin'):
        msg = '你还未登陆，请先登陆！'
        return render(req, 'error_msg.html', locals())
    if req.method == 'GET':
        goods = Goodsissue.objects.get(id=goods_id)
        # 判断商品是否属于本人以决定赋予编辑权限与否
        if goods.owner_id == req.session['user_info']['uid']:
            isowner = True
        # 评论母表
        msg_ces = MessageCompose.objects.filter(goods=goods)
        msg_ces_num = len(msg_ces)
        msg_cts_list = []
        # 评论子表
        for i in range(msg_ces_num):
            msg_cts = MessageComment.objects.filter(reply_from=msg_ces[i])
            msg_cts_list.append(msg_cts)
        return render(req, 'goods/goods_detail.html', locals())
    # 响应留言操作(将留言保存在数据库)
    data = req.POST
    message_infos = {}
    message_infos["uid_id"] = req.session['user_info']['uid']
    message_infos["messagedate"] = fun.now()
    message_infos["content"] = data.get('message_content')
    if data['reply_from']:
        # 需要更改modelform，并且区别评论母子表，删除评论栏模块
        message_infos["reply_from"] = data.get('reply_from')
        message_infos["reply_to"] = data.get('reply_to')
        MessageComment.objects.create(**message_infos)
    else:
        message_infos["goods_id"] = goods_id
        MessageCompose.objects.create(**message_infos)
    return HttpResponseRedirect(f"goodsDetail/{goods_id}")

#评论栏模块
def message(req):
    if not req.session.get('islogin'):
        msg = '你还未登陆，请先登陆！'
        return render(req,'error_msg.html', locals())
    if req.method == 'GET':
        uid = req.session['user_info']['uid']

        #通过用户id获取其发布的商品id
        p = Goodsissue.objects.filter(owner_id=uid)
        if not p:
            msg = '你还未上架任何商品！'
            return render(req,'error_msg.html', locals())

        #定义一个送信人id的列表
        messager_infos = []

        #通过商品id获取该栏下留言
        for goods in p:
            goods_id = goods.id
            p2 = MessageCompose.objects.filter(goods_id=goods_id)
            if p2:
                for p in p2:
                #因为二级list无法作为迭代器，因此使用元组
                    messager_infos.append((p.uid, goods_id))

        #对list中的数据进行去重工作
        messager_infos = list(set(messager_infos))
        #跨APP调用trade子模块中controller中的方法，传入一个列表对象
        result = controller.get_gooods_message(messager_infos)
        return render(req,'message_log.html', locals())