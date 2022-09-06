from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    # 主页
    path('', views.index),

    # 搜索
    path('search/<str:during>', views.search),

    # 控制台（django默认）
    path('admin/', admin.site.urls),

    # 用户相关模块
    path('userIssue/', include('userIssue.urls',namespace = "userIssue")),

    # 商品相关模块
    path('goodsIssue/', include('goodsIssue.urls',namespace = "goodsIssue")),

    # 奇奇怪怪的附加模块
    path('others/', include('others.urls',namespace = "others")),

    # 消息中心模块
    path('message/',views.message),

    # 系统通知模块
    path('sys_message/',views.sys_message),

    # 图片显示模块
    path('image/upload/<str:image_name>/', views.get_img)
    
]

