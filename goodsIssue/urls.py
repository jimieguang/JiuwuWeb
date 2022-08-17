app_name = "goodsIssue_urls"

from django.urls import path, include,re_path
from . import views

urlpatterns = [
        path('newGoods', views.newGoods),
        path('myGoods/<str:during>', views.myGoods),
        path('goodsList/<str:during>', views.goodsList),
        path('goodsDetail/<int:goods_id>', views.goodsDetail),
]