from django.shortcuts import render
from django.template import RequestContext
from django.forms import ModelForm
from django.http import HttpResponseRedirect
# 数据库模型
from userIssue.models import User, PrivateMessage
from goodsIssue.models import Goodsissue, MessageCompose, MessageComment
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
    goods_num = goods_infos.count()
    return render(req, 'goods/goods_list.html', locals())


#消息中心模块
def message(req,type):
    uid = req.session.get('user_info')["uid"]
    user = User.objects.get(id=uid)
    # 取得各类型未读信息的数量
    private_messages = PrivateMessage.objects.filter(pm_to_id=uid)
    private_messages_unread = private_messages.filter(isRead=False)
    private_messages_unread_num = private_messages_unread.count()
    msg_ces = MessageCompose.objects.filter(owner_id=uid)
    msg_ces_unread_num = msg_ces.filter(isRead=False).count()
    msg_cts = MessageComment.objects.filter(reply_from_id=uid)
    msg_cts_unread_num = msg_cts.filter(isRead=False).count()
    
    if type == 'my_news':
        users = []
        last_messages = []
        unread_nums = []
        for private_message in private_messages:
            if private_message.pm_from not in users:
                users.append(private_message.pm_from)
                unread_messages = private_messages_unread.filter(pm_from=private_message.pm_from)
                last_messages.append(unread_messages.last())
                unread_nums.append(unread_messages.count())
        
    elif type == 'goods_comment':
        msg_ces = msg_ces.order_by('-messagedate')
    elif type == 'reply':
        msg_cts = msg_cts.order_by('-messagedate')
    return render(req, '/message.html',locals())



    
    