from django.urls import path, re_path
from . import views

urlpatterns = [
    path('addhosts/', views.add_hosts, name='add_hosts'),
    path('addmodules/', views.add_modules, name='add_modules'),
    path('tasks/', views.tasks, name='tasks'),
    path('result/', views.result, name='result'),
    re_path('^del_arg/(?P<pk_id>[0-9]+)/(?P<flag>[0-9]+)/$', views.del_arg, name='del_arg'),
    re_path('', views.host_info, name="host_info"),
]
