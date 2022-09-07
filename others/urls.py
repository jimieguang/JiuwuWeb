app_name = "others_urls"

from django.urls import path
from . import views

urlpatterns = [
        path('printer', views.printer),
]