from django.db import models
from userIssue.models import User 

# Create your models here.
class Goodsissue(models.Model):
    '''商品表'''
    # id是django自动创建的，故不需要显式定义
    # id = models.IntegerField(primary_key=True)
    # 必填（非空）
    owner = models.ForeignKey(User, blank=False,on_delete=models.CASCADE)
    name = models.CharField(verbose_name="商品名称",max_length=255, blank=False)
    price = models.FloatField(verbose_name="售卖价格",blank=False)     # 售卖价格
    issuedate = models.DateTimeField(verbose_name="发布时间",db_column='issueDate', blank=False)
    # 选填（可为空）
    buy_price = models.FloatField(verbose_name="购入价格",blank=True,null=True)  # 购入价格
    introduction = models.CharField(verbose_name="介绍",max_length=255, blank=True)
    imagefile = models.ImageField(verbose_name="图片",max_length=255, blank=True)

    class Meta:
        verbose_name = "商品"
        verbose_name_plural = "商品"

    def __str__(self):
        return self.name

class MessageCompose(models.Model):
    '''商品留言表（母表）'''
    # id是django自动创建的，故不需要显式定义
    # id = models.IntegerField(primary_key=True)
    # 必填（非空）
    owner = models.ForeignKey(User, db_column='uid', blank=False, on_delete=models.CASCADE)
    goods = models.ForeignKey(Goodsissue, blank=False,on_delete=models.CASCADE)
    messagedate = models.DateTimeField(verbose_name="留言时间",db_column='messageDate', blank=False)
    content = models.TextField(verbose_name="留言内容",max_length=255, db_column='content', blank=False)
    isRead = models.BooleanField(default=False, verbose_name="已读？", db_column='isRead')
    # 选填（可为空）

    class Meta:
        verbose_name = "留言"
        verbose_name_plural = "商品留言"
        
    def __str__(self):
        return self.content

class MessageComment(models.Model):
    '''商品评论表（子表）'''
    # id是django自动创建的，故不需要显式定义
    # id = models.IntegerField(primary_key=True)
    # 必填（非空）
    owner = models.ForeignKey(User, db_column='uid', blank=False, on_delete=models.CASCADE)
    reply_from = models.ForeignKey(MessageCompose, blank=False, on_delete=models.CASCADE)    #母表
    messagedate = models.DateTimeField(verbose_name="留言时间",db_column='messageDate', blank=False)
    content = models.TextField(verbose_name="留言内容",max_length=255, db_column='content', blank=False)
    isRead = models.BooleanField(default=False, verbose_name="已读？", db_column='isRead')
    # 选填（可为空）
    reply_to = models.ForeignKey(User, related_name='reply_to', blank=True, null=True,on_delete=models.CASCADE)

    class Meta:
        verbose_name = "留言的评论"
        verbose_name_plural = "留言评论"
        
    def __str__(self):
        return self.content
