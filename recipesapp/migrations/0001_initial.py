# Generated by Django 2.0.4 on 2018-04-15 07:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hashtags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=51, verbose_name='хештег')),
            ],
            options={
                'ordering': ['recipes', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Recipes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='наименование блюда')),
                ('description', models.TextField(verbose_name='полное описание')),
                ('img_big', models.ImageField(blank=True, upload_to='big', verbose_name='изображение (большое)')),
                ('img_small', models.ImageField(blank=True, upload_to='preview', verbose_name='изображение (маленькое)')),
                ('typeof', models.CharField(choices=[('1', 'салат'), ('2', 'первое'), ('3', 'второе'), ('4', 'суп'), ('5', 'десерт'), ('6', 'напиток')], default='1', max_length=1, verbose_name='тип блюда')),
                ('likes', models.PositiveIntegerField(blank=True, default=0, verbose_name='лайки')),
                ('is_active', models.BooleanField(default=True, verbose_name='активность')),
                ('create_date', models.DateField(auto_now_add=True, verbose_name='дата создания')),
                ('update_date', models.DateField(auto_now=True, verbose_name='дата обновления')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RecipesStep',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idx', models.PositiveIntegerField(verbose_name='шаг')),
                ('step', models.TextField(verbose_name='полное описание')),
                ('recipes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipesapp.Recipes', verbose_name='рецепт')),
            ],
            options={
                'ordering': ['idx', 'recipes'],
            },
        ),
        migrations.AddField(
            model_name='hashtags',
            name='recipes',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipesapp.Recipes', verbose_name='рецепт'),
        ),
    ]
