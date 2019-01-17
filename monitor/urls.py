#monitor url
from django.urls import path, re_path
from . import views as monitor_views

app_name = 'monitor'
urlpatterns = [
    path('', monitor_views.index),
]