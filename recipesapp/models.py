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
    likes = models.PositiveIntegerField(
        verbose_name='лайки',
        default=0,
        blank=True,
        null=False)
    is_active = models.BooleanField(
        verbose_name = 'активность',
        default=True)
    create_date = models.DateField(
        verbose_name='дата создания',
        auto_now_add=True)
    update_date = models.DateField(
        verbose_name='дата обновления',
        auto_now=True)

    @property
    def get_typeof_str(self):
        result = list(filter(lambda x: x == self.typeof, Recipes.typeof_choices))
        if result:
            return result[0][1]
        else:
            return ''

    @classmethod
    def get_typeof_choices(cls):
        return cls.typeof_choices

    

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

    @property
    def get_hashtag_by_recipes(self):
        return Hashtags.objects.filter(recipes=self.recipes)

    @property
    def get_all_hashtags(self):
        return Hashtags.objects.all().values("name").distinct()