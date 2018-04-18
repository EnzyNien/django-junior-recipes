from django.urls import include, re_path
from mainapp import views

app_name = 'mainapp'

urlpatterns = [
	re_path(r'^$', views.main, name='main'),
]
