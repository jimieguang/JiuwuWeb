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
    # 登陆与否
    isLogin = req.session.get('islogin')
    if isLogin == True:
        uid = req.session.get('user_info')["uid"]
        user = User.objects.get(id=uid)
        name = user.name
        avatar = user.avatar
        # 显示未读消息数量(filter筛选时，双下划线表示查询相关数据的属性)
        private_messages_unread_num = PrivateMessage.objects.filter(pm_to_id=uid,isRead=False).count()
        msg_ces_unread_num = MessageCompose.objects.filter(goods__owner_id=uid,isRead=False).count()
        msg_cts_unread_num = (MessageComment.objects.filter(reply_to__owner_id=uid,isRead=False) | MessageComment.objects.filter(reply_from__owner_id=uid,reply_to__isnull=True,isRead=False)).count()
        total_unread_num = private_messages_unread_num + msg_ces_unread_num + msg_cts_unread_num
    else:
        total_unread_num = 0
        system_message_num = 1
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
def message(req):
    uid = req.session.get('user_info')["uid"]
    user = User.objects.get(id=uid)
    # 取得各类型未读信息的数量
    private_messages = PrivateMessage.objects.filter(pm_to_id=uid)
    private_messages_unread = private_messages.filter(isRead=False)
    private_messages_unread_num = private_messages_unread.count()
    msg_ces = MessageCompose.objects.filter(goods__owner_id=uid).order_by('-messagedate')
    msg_ces_unread = msg_ces.filter(isRead=False)
    msg_ces_unread_num = msg_ces_unread.count()
    msg_cts = (MessageComment.objects.filter(reply_to__owner_id=uid) | MessageComment.objects.filter(reply_from__owner_id=uid,reply_to__isnull=True)).order_by('-messagedate')
    msg_cts_unread = msg_cts.filter(isRead=False)
    msg_cts_unread_num = msg_cts_unread.count()
    #对'回复我的'以及'商品评价'进行已读处理
    msg_ces_unread.update(isRead=True)
    msg_cts_unread.update(isRead=True)
    # 返回非重复用户信息（reply_from)及消息预览
    users = []
    last_messages = []
    unread_nums = []
    for private_message in private_messages:
        if private_message.pm_from not in users:
            users.append(private_message.pm_from)
            unread_messages = private_messages_unread.filter(pm_from=private_message.pm_from)
            last_messages.append(unread_messages.last())
            unread_nums.append(unread_messages.count())
    my_news = zip(users,unread_nums,last_messages)
    return render(req, 'message.html',locals())

# 系统通知模块
def sys_message(req):
    return render(req, 'system_msg.html', locals())