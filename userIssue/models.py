from django.db import models
from dtiaozao.settings import BASE_DIR


class User(models.Model):
    '''用户表'''
    # id是django自动创建的，故不需要显式定义
    # id = models.IntegerField(primary_key=True)
    # 必填（非空）
    student_id = models.IntegerField(verbose_name="学号",blank=False, unique=True)   # 学号是用户的唯一凭证
    passwd = models.CharField(verbose_name="密码",max_length=255, blank=False)
    name = models.CharField(verbose_name="昵称",max_length=255, blank=False)
    # 选填（可为空）
    avatar = models.ImageField(verbose_name="头像",max_length=255, blank=True)
    signature = models.CharField(verbose_name="个性签名",max_length=255, blank=True)
    phone = models.IntegerField(verbose_name="手机号", blank=True,null=True)
    email = models.EmailField(verbose_name="邮箱",max_length=255, blank=True)

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"  #复数形式

    def __str__(self):
        return self.name

class PrivateMessage(models.Model):
    '''私聊信息表'''
    # 必填（非空）
    pm_from = models.ForeignKey(User,related_name = "pm_from",verbose_name="发信人", blank=False,on_delete=models.CASCADE)    #外链仅储存id，不占用额外数据库资源
    pm_to = models.ForeignKey(User,related_name = "pm_to",verbose_name="收信人", blank=False,on_delete=models.CASCADE)        
    messagedate = models.DateTimeField(verbose_name="私聊时间",db_column='messageDate', blank=False)
    content = models.TextField(verbose_name="私聊内容",max_length=255, db_column='content', blank=False)
    isRead = models.BooleanField(default=False, verbose_name="已读？", db_column='isRead')
    # 选填（可为空）

    class Meta:
        verbose_name = "私聊信息"
        verbose_name_plural = "私聊信息"  #复数形式

    def __str__(self):
        return self.content

