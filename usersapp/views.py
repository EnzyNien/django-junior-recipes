from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from django.contrib import auth
from django.conf import settings
from django.contrib.auth.models import AnonymousUser

#from usersapp.forms import LoginForm, RegisterForm, EditForm, GenForm
from usersapp.models import RecipesUser


def login(request, *args, **kwargs):
    return HttpResponse('login')

def logout(request, *args, **kwargs):
    return HttpResponse('logout')

def registration(request, *args, **kwargs):
    return HttpResponse('registration')