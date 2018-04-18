from functools import wraps
from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.list import ListView

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test

from recipesapp.models import Recipes

from mainapp.decorators import add_userdata_to_context

#@add_userdata_to_context
#def recipes_my_typeof(request,*args,**kwargs):
#    typeof = kwargs.get('typeof', -1)
#    user = recipes_my_typeof.context['user']
#    recipes_my_typeof.context['object_list'] = Recipes.objects.filter(typeof=typeof, author=user)
#    recipes_my_typeof.context['typeof_choices'] = Recipes.get_typeof_choices()
#    return render(request, 'recipesapp/all.html', recipes_my_typeof.context)

@add_userdata_to_context
def recipes_my(request,*args,**kwargs):
	return HttpResponse('recipes_my')

@add_userdata_to_context
def recipes_all_typeof(request,*args,**kwargs):
    typeof = kwargs.get('typeof', -1)
    recipes_all_typeof.context['object_list'] = Recipes.objects.filter(typeof=typeof)
    recipes_all_typeof.context['typeof_choices'] = Recipes.get_typeof_choices()
    recipes_all_typeof.context['typeof_menu_item'] = int(typeof)
    return render(request, 'recipesapp/all.html', recipes_all_typeof.context)

class RecipesAll(ListView):

    model = Recipes
    template_name = 'recipesapp/all.html'

    #def dispatch(self, *args, **kwargs):
    #    return super().dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['typeof_choices'] = Recipes.get_typeof_choices()
        context['typeof_menu_item'] = -1
        return context

@add_userdata_to_context
def recipes_filter(request,*args,**kwargs):
	return HttpResponse('recipes_filter')

@add_userdata_to_context
def recipe(request,*args,**kwargs):
	return HttpResponse('recipe')