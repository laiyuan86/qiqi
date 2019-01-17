#logs url
from django.urls import path, re_path
from . import views as logs_view


app_name = 'logs'
urlpatterns = [
    path('', logs_view.index),
]