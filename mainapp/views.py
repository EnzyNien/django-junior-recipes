from functools import wraps
from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ObjectDoesNotExist

from mainapp.decorators import add_userdata_to_context

@add_userdata_to_context
def main(request,*args,**kwargs):
    return redirect('recipes:all', permanent=True, typeof=0)
