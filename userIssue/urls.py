app_name = "userIssue_urls"

from django.urls import path
from . import views

urlpatterns = [
    path('mySpace/<int:uid>/', views.mySpace),
    path('login/', views.login),
    path('logout/', views.logout),
    path('PM/<int:with_uid>/', views.private_message),
]