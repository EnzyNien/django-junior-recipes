import json
import os
import random
from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ObjectDoesNotExist

def main(request,*args,**kwargs):
	return render(request, 'mainapp/index.html')

