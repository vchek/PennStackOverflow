from django.urls import path, re_path
from . import views

app_name = 'userpage'

urlpatterns = [
    re_path('^(?P<username>[a-zA-Z0-9_]+)/$', views.profile, name='profile'),
    re_path('^(?P<username>[a-zA-Z0-9_]+)/graph$', views.graph, name='graph'),
    re_path('^(?P<username>[a-zA-Z0-9_]+)/password$', views.change_password, name='change_password'),
    re_path('^(?P<username>[a-zA-Z0-9_]+)/picture$', views.change_picture, name='change_picture'),
]
