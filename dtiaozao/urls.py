from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    # 主页
    path('', views.index),

    # 搜索
    path('search/<str:during>', views.search),

    # 个人中心
    path('self/', views.self),

    # 控制台（django默认）
    path('admin/', admin.site.urls),

    # 用户相关模块
    path('userIssue/', include('userIssue.urls',namespace = "userIssue")),

    # 商品相关模块
    path('goodsIssue/', include('goodsIssue.urls',namespace = "goodsIssue")),
    
]

