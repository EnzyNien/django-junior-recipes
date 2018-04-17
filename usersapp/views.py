
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404, Http404
from django.urls import reverse
from django.contrib import auth
from django.conf import settings
from django.contrib.auth.models import AnonymousUser

from usersapp.forms import LoginForm, RegistrationForm
from usersapp.models import RecipesUser
from mainapp.decorators import user_login

@user_login
def login(request, *args, **kwargs):
    form = LoginForm()
    if request.method == 'POST':
            form = LoginForm(data=request.POST)
            if form.is_valid():
                username_list = RecipesUser.objects.filter(nickname=request.POST['username'])
                if not username_list:
                    raise Http404("price search error")
                else:
                    username = username_list[0].username
                    password = request.POST['password']
                user = auth.authenticate(username=username, password=password)
                if user and user.is_active:
                    auth.login(request, user)
                    other_ref = request.POST.get('ref',None)
                    return HttpResponseRedirect(other_ref)
    context = {
        'form_title': "Авторизация на портале",
        'form': form,
    }
    return render(request, 'usersapp/universal.html', context)

def logout(request, *args, **kwargs):
    return HttpResponse('logout')

def registration(request, *args, **kwargs):
    form = RegistrationForm()
    if request.method == 'POST':
            form = RegistrationForm(data=request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('auth:login'))
    context = {
        'form_title': "Регистрация на портале",
        'form': form,
        'registration':True
    }
    return render(request, 'usersapp/universal.html', context)