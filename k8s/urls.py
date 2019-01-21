#k8s url

from django.urls import path, re_path
from . import views as k8s_view

app_name = 'k8s'
urlpatterns = [
    path('', k8s_view.index),
    re_path(r'pods/.', k8s_view.get_pods_by_ns),
    re_path(r'nodes/.', k8s_view.get_node_info_by_nodename),
]