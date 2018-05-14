from django.urls import include, re_path
from usersapp import views

app_name = 'usersapp'

urlpatterns = [
    re_path(r'^$', views.login),
    re_path(r'^login/$', views.login, name='login'),
    re_path(r'^logout/$', views.logout, name='logout'),
    re_path(r'^registration/$', views.registration, name='registration'),
    re_path(r'^room/$', views.room, name='room'),
]


