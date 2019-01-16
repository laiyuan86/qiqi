#harbor urls

from django.urls import path, re_path
from . import views as harbor_view

app_name = 'harbor'
urlpatterns = [
    path('', harbor_view.index, name="harbor_index"),
    path('about/', harbor_view.about, name='harbor_about'),
    re_path(r'detail/.', harbor_view.get_pm_detail),
    path('tags/', harbor_view.get_image_tags),
    path('delete/', harbor_view.delete_image),
    re_path(r'tags/.', harbor_view.get_image_tags),
]