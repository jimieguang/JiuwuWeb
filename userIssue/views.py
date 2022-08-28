#encoding: utf-8
from django import forms
from django.forms import ModelForm
from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect
import json

from userIssue.models import User
from userIssue.models import PrivateMessage

import dtiaozao.function as fun

class Userform(ModelForm):
    class Meta:
        model = User
        fields = ["name","avatar","signature","phone","email"]
        
class LoginForm(forms.Form):
    '''登录表单'''
    student_id = forms.IntegerField(
        label = "学号",
        required = True  # 表示必填项
    )
    passwd = forms.CharField(
        label = "密码",
        widget = forms.PasswordInput,
        required = True
    )
    def clean_passwd(self):
        # 钩子函数，用于修改from中passwd的返回值（加密后）
        return fun.mk_md5(self.cleaned_data.get("passwd"))

class RegisterForm(ModelForm):
    # 定义父类以外的元素
    confirm_passwd = forms.CharField(
        label = "确认密码",
        widget = forms.PasswordInput,
    )
    class Meta:
        model = User
        fields = ["student_id","passwd","confirm_passwd","name","phone","email"]
        # 此处修改type
        widgets = {
            "passwd":forms.PasswordInput
        }
    def clean_passwd(self):
        '''数据库中的密码是经过加密的'''
        passwd = self.cleaned_data["passwd"]
        return fun.mk_md5(passwd)

    def clean_confirm_passwd(self):
        """钩子函数：用于自定义数据返回值以替换cleaned_data中的值（也可用于数据校验）"""
        passwd = self.cleaned_data["passwd"]
        confirm_passwd = fun.mk_md5(self.cleaned_data["confirm_passwd"])
        if confirm_passwd != passwd:
            raise forms.ValidationError("密码不一致")
        return confirm_passwd

class PMform(ModelForm):
    class Meta:
        model = PrivateMessage
        fields = ["content","image"]
#个人中心模块
def mySpace(req,uid):
    if req.method == 'GET':
        user = User.objects.get(id=uid)
        isOwner = (uid == req.session['user_info']['uid'])
        return render(req,'user/self.html',locals())
    # 修改个人信息
    uid = req.session.get('user_info')['uid']
    obj = User.objects.get(id=uid)
    # req.POST默认不可修改，所以需要“副本”
    data = req.POST.copy()
    data["name"] = data['name'] if data['name']!="" else obj.name
    data["signature"] = data['signature'] if data["signature"]!="" else obj.signature
    form = Userform(data = data,instance = obj)
    if form.is_valid():
        # 实例化modelform，提交前对用户属性进行更改
        form = form.save(commit=False)
        if data["imagefile"]:
            obj.avatar.delete()     #删除原头像文件
            form.avatar = fun.save_image(data["imagefile_name"],data["imagefile"])
        form.save()
        return HttpResponseRedirect('./')
    msg = '表单格式有误'
    return render(req, 'error_msg.html', locals())

#登录模块
def login(req):
    # 登录注册界面
    if req.method == 'GET':
        return render(req,'user/login.html', locals())
    data = req.POST
    # 响应登录post
    if data["action"] == "login":
        form = LoginForm(data = req.POST)
        if form.is_valid():
            user_obj = User.objects.filter(**form.cleaned_data).first()
            if not user_obj:
                form.add_error("passwd","用户名或密码错误")
                msg = "用户名或密码错误（数据库验证）"
                return render(req,'error_msg.html', locals())
            #登录成功后，将用户信息添加到session中
            req.session['islogin'] = True
            user_info = {}
            user_info['uid'] = user_obj.id
            user_info['name'] = user_obj.name
            user_info['student_id'] = user_obj.student_id
            req.session['user_info'] = user_info
            return HttpResponseRedirect('/')
        msg = form.errors
        return render(req,'error_msg.html', locals())
    # 响应注册post
    form = RegisterForm(data=req.POST)
    if form.is_valid():
        form.save()
        msg = '注册成功，请返回首页后登录！'
        return HttpResponseRedirect('/userIssue/login')
    # 携带错误信息返回
    return render(req,'user/login.html', locals())


#登出模块
def logout(req):
    if req.method == 'POST':
        msg = '非法访问！！'
        return render(req,'error_msg.html', locals())
    #删除session信息
    del req.session['user_info']
    del req.session['islogin']
    return HttpResponseRedirect('/')


#私聊模块
def private_message(req,with_uid):
    Alice = User.objects.get(id = req.session['user_info']['uid'])
    Black = User.objects.get(id=with_uid)
    if req.method == 'GET':
        # 将私聊信息按时间排序/合并
        A2Bs = PrivateMessage.objects.filter(pm_from = Alice,pm_to = Black).order_by('messagedate')
        B2As = PrivateMessage.objects.filter(pm_from = Black,pm_to = Alice).order_by('messagedate')
        messages = A2Bs | B2As
        pastdate = messages.last().messagedate.strftime("%Y-%m-%d %X") if messages.count()!=0 else fun.now()
        # 对私聊信息进行已读处理
        B2As.update(isRead=True)
        return render(req,"user/chat.html",locals())
    if req.POST.get("refresh"):
        # 轮询同步信息时仅需关注对方发来的信息
        start = fun.str2datetime(req.POST.get("pastdate"),1)
        end = fun.now()
        B2As = PrivateMessage.objects.filter(pm_from = Black,pm_to = Alice,messagedate__range = [start,end]).order_by('messagedate')
        pastdate = B2As.last().messagedate.strftime("%Y-%m-%d %X") if B2As.last() else end
        response_dict = {"length":B2As.count(),"messagedate":[],"pastdate":pastdate,"content":[],"image_name":[]}
        for B2A in B2As:
            response_dict["content"].append(B2A.content)
            response_dict['image_name'].append(B2A.image.name if B2A.image else "")
            response_dict["messagedate"].append(B2A.messagedate.strftime("%Y-%m-%d %X"))
        return HttpResponse(json.dumps(response_dict))
    # 将自己发送的信息保存到数据库
    data = req.POST
    if req.POST.get('content')=="" and req.POST.FILES=="":
        return HttpResponse(json.dumps({'error':"Empty content!"}))
    form = PMform(data=data,files=req.FILES)
    form = form.save(commit=False)   #获得返回值以修正modelform数据，非正式提交
    form.pm_from = Alice
    form.pm_to = Black
    form.messagedate = fun.now()
    form.save()                      #正式创建表
    return HttpResponse(json.dumps({'status':200}))


