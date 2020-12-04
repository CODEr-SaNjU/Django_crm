from django.shortcuts import render,redirect , get_object_or_404
from django.contrib.auth.models import User,auth ,Group
from django.http import Http404, HttpResponse
# Create your views here.


def login(request):
    return render(request,'html_files/login.htm')