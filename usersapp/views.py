from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404, Http404, redirect
from django.urls import reverse
from django.conf import settings

from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.decorators import login_required
from django.contrib import auth

from usersapp.forms import LoginForm, RegistrationForm, ChangeForm
from usersapp.models import RecipesUser

from mainapp.decorators import add_userdata_to_context


@add_userdata_to_context
def login(request, *args, **kwargs):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = RecipesUser.objects.get(
                nickname=request.POST['username'])
            username = username.username
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return redirect('recipes:all', permanent=True, typeof=0)
    login.context = {
        'form_title': "Авторизация на портале",
        'form': form,
    }
    return render(request, 'usersapp/universal.html', login.context)

def logout(request, *args, **kwargs):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))

def registration(request, *args, **kwargs):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            if user and user.is_active:
                auth.login(request, user)
            context = {
                'form_title': "Регистрация на портале",
                'user_id': user.user_id
            }
            return render(request, 'usersapp/action_approved.html', context)
    context = {
        'form_title': "Регистрация на портале",
        'form': form,
        'registration': True
    }
    return render(request, 'usersapp/universal.html', context)

@add_userdata_to_context
@login_required
def room(request, *args, **kwargs):
    user = request.user
    if request.method == "POST":
        form = ChangeForm(data=request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect('main')
        else:
            room.context.update({
                'form': form,
                'form_title': 'Редактирование данных'
            })
            return render_to_response('usersapp/room.html', room.context)
    else:
        form = ChangeForm(instance=user)
        room.context.update({
            'form': form,
            'form_title': 'Редактирование данных'
        })
        return render(request, "usersapp/room.html", room.context)
