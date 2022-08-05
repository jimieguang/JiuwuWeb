#encoding: utf-8
from userIssue.models import User
from goodsIssue.models import Goodsissue, MessageCompose, MessageComment
from dtiaozao import function as fun


#从数据库中取得商品信息
def get_goods(uid):
    #扫描商品表
    owner_id = User.objects.get(id=uid)
    u = Goodsissue.objects.filter(owner_id=owner_id)
    return u


#商品下架处理
def del_goods(data):
    goods_id = data['id']
    p = Goodsissue.objects.get(id=goods_id)
    if p:
        p.delete()
    else:
        return -1


#商品评论信息获取
def get_gooods_message(messager_infos):
    result = []
    info = {}
    for messager_info in messager_infos:
        #判断是购买功能还是售出功能传入的参数
        if messager_info[1]:
            u = MessageCompose.objects.filter(uid=messager_info[0], goods_id=messager_info[1])

        #购买与售出的公共模块
        if u:
            for message in u:
                info['goods_id'] = message.goods_id
                info['messager_name'] = message.uid.name
                info['message_date'] = message.messagedate
                info['message_content'] = message.content
                p = Goodsissue.objects.get(id=message.goods_id)
                info['goods_name'] = p.name
                info['goods_owner'] = p.owner.name
                result.append(info)
                info = {}
    #对结果集进行排序，以销售日期的先后做排序(注：该函数无返回值)
    result.sort(key=lambda item: item['message_date'], reverse=True)
    return result