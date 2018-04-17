from functools import wraps
from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ObjectDoesNotExist

from mainapp.decorators import user_login

@user_login
def main(request,*args,**kwargs):
	return render(request, 'mainapp/index.html', main.context)

