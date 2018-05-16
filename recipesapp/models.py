import os
import json

from django.db import models
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from usersapp.models import RecipesUser

''' 
Рецепт: 
+название, 
+описание, 
+шаги приготовления, 
+фотография конечного блюда, 
+тип блюда (салат, первое, второе, суп, десерт, напиток), 
автор, 
+лайки, 
+набор хештегов, 
+статус (активный, заблокирован), 
+дата создания,
+дата обновления.
'''
#категории
class Recipes(models.Model):

    typeof_choices = (
        ('1', 'салат'),
        ('2', 'первое'),
        ('3', 'второе'),
        ('4', 'суп'),
        ('5', 'десерт'),
        ('6', 'напиток'),)

    name = models.CharField(
        verbose_name = 'наименование блюда', 
        max_length=100, 
        blank=False)
    description = models.TextField(
        verbose_name = 'полное описание', 
        blank=True)
    description_short = models.CharField(
        verbose_name = 'краткое описание', 
        max_length = 100,
        blank=True)
    img_big = models.ImageField(
        verbose_name = 'изображение (большое)', 
        upload_to=settings.BIG_IMG_DIR,
        blank=True)
    img_small= models.ImageField(
        verbose_name = 'изображение (маленькое)', 
        upload_to=settings.SMALL_IMG_DIR,
        blank=True)
    typeof = models.CharField(
        verbose_name = 'тип блюда',
        max_length=1,
        choices=typeof_choices,
        default = '1',
        blank=False)
    author = models.ForeignKey(
        RecipesUser, 
        on_delete=models.CASCADE,
        blank=False)
    #likes = models.PositiveIntegerField(
    #    verbose_name='лайки',
    #    default=0,
    #    blank=True,
    #    null=False)
    is_active = models.BooleanField(
        verbose_name = 'активность',
        default=True)
    create_date = models.DateTimeField(
        verbose_name='дата создания',
        auto_now_add=True)
    update_date = models.DateTimeField(
        verbose_name='дата обновления',
        auto_now=True)

    @property
    def get_typeof_str(self):
        result = list(filter(lambda x: x[0] == self.typeof, Recipes.typeof_choices))
        if result:
            return result[0][1]
        else:
            return ''

    @classmethod
    def get_typeof_choices(cls):
        return cls.typeof_choices

class Likes(models.Model):

    recipes = models.ForeignKey(
        Recipes, 
        verbose_name = 'рецепт',
        on_delete=models.CASCADE)
    user = models.ForeignKey(
        RecipesUser, 
        on_delete=models.CASCADE,
        blank=False)

    @staticmethod
    def get_likes_by_recipes(recipes):
        return Likes.objects.filter(recipes = recipes).count()

    @staticmethod
    def get_likes_by_recipe_pk(pk):
        return Likes.objects.filter(recipes__pk = pk).count()

    @staticmethod
    def click(pk, user):
        new_like = None
        already_exists = False
        error = False
        try:
            resipe_obj = Recipes.objects.get(pk=pk)
            like = Likes.objects.filter(recipes = resipe_obj, user=user)
        except ObjectDoesNotExist:
            error = True
        else:
            if like:
                already_exists = True
                like.delete()
            else:
                try:
                    new_like = Likes(recipes=resipe_obj,user=user)
                    new_like.save()
                except:
                    error = True
            count = Likes.get_likes_by_recipes(resipe_obj)
        return {'error':error,'already_exists':already_exists,'count':count}

class RecipesStep(models.Model):

    recipes = models.ForeignKey(
        Recipes, 
        verbose_name = 'рецепт',
        on_delete=models.CASCADE)
    idx = models.PositiveIntegerField(
        verbose_name = 'шаг',
        blank=False)
    step = models.TextField(
        verbose_name = 'полное описание', 
        blank=False)
    
    class Meta():
        ordering = ['idx','recipes']

class Hashtags(models.Model):
    
    name = models.CharField(
        verbose_name = 'хештег', 
        max_length=51, 
        blank=False)
    recipes = models.ForeignKey(
        Recipes, 
        verbose_name = 'рецепт',
        on_delete=models.CASCADE)

    class Meta():
        ordering = ['recipes','name']

    @staticmethod
    def get_hashtag_by_recipe(recipe):
        return Hashtags.objects.filter(recipes=recipe)

    #def get_hashtag_by_recipe(self, recipes):
    #    for r in recipes:
    #    return Hashtags.objects.filter(recipes=recipe)

    @property
    def get_all_hashtags(self):
        return Hashtags.objects.all().values("name").distinct()