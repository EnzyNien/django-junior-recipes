from django.urls import include, re_path
from recipesapp import views

app_name = 'recipesapp'

urlpatterns = [
    #re_path(r'^my/(?P<typeof>\d+)/$', views.recipes_my, name='my'),
    re_path(r'^all/(?P<typeof>\d+)/$', views.recipes_all_typeof, name='all_typeof'),
    re_path(r'^my/$', views.recipes_my, name='my'),
    re_path(r'^all/$', views.RecipesAll.as_view(), name='all'),
    #re_path(r'^filter/$', views.recipes_filter, name='filter'),
    re_path(r'^recipe/(?P<pk>\d+)/$', views.recipe, name='recipe'),
]


