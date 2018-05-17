from functools import wraps
from django.shortcuts import render, HttpResponse, Http404
from django.http import JsonResponse

from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.decorators import user_passes_test

from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.list import ListView

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404

from recipesapp.models import Recipes, Hashtags, Likes, RecipesStep

from mainapp.decorators import add_userdata_to_context

def return_user_recipes(user, query_set):
    return query_set.filter(author = user)

def return_typeof_recipes(typeof, query_set):
    return query_set.filter(typeof = typeof)

class Recipe_Base(ListView):

    model = Recipes
    template_name = 'recipesapp/all.html'

    def dispatch(self, *args, **kwargs):
        self.userdata = {
			'user':args[0].user,
			'is_authenticated':args[0].user.is_authenticated
		}
        self.typeof = int(kwargs.get('typeof', 0))
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        self.context = super().get_context_data(*args, **kwargs)
        self.context['typeof_choices'] = Recipes.get_typeof_choices()
        self.context['typeof_menu_item'] = int(self.typeof)
        self.context.update(self.userdata)
        if not self.typeof == 0:
            self.context['object_list'] = return_typeof_recipes(self.typeof, self.context['object_list'])

class RecipesMy(Recipe_Base):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        super().get_context_data(*args, **kwargs)
        self.context['object_list'] = return_user_recipes(self.context['user'], self.context['object_list'])
        self.context['my'] = True
        return self.context

class RecipesAll(Recipe_Base):

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        super().get_context_data(*args, **kwargs)
        return self.context

class RecipesEdit(Recipe_Base):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        super().get_context_data(*args, **kwargs)
        self.context['object_list'] = return_user_recipes(self.context['user'], self.context['object_list'])
        self.context['my'] = True
        return self.context

@add_userdata_to_context
def recipes_filter(request,*args,**kwargs):
	return HttpResponse('recipes_filter')

@add_userdata_to_context
def recipe(request,*args,**kwargs):
    pk = kwargs.get('pk',-1)
    item = get_object_or_404(Recipes, pk=pk)
    recipe.context['item'] = item
    recipe.context['hashtag'] = Hashtags.get_hashtag_by_recipe(item)
    recipe.context['steps'] = RecipesStep.get_steps_by_recipe(item) 
    return render(request, 'recipesapp/recipe.html', recipe.context)

@add_userdata_to_context
def like(request,*args,**kwargs):
    if request.is_ajax():
        if request.method == 'POST':
            user = like.context['user']
            pk = request.POST.get('id',None)
            if user.is_authenticated:
                result = Likes.click(pk,user)
            else:
                return Http404()
            return JsonResponse(result) 
        elif request.method == 'GET': 
            pk = request.GET.get('id',None)
            try:
                result = Likes.get_likes_by_recipe_pk(pk)
            except:
                result = 0
            return JsonResponse({'count':result})