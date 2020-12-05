from django.shortcuts import render,redirect , get_object_or_404
from django.contrib.auth.models import User,auth ,Group
from django.http import Http404, HttpResponse
from django.shortcuts import render,redirect , get_object_or_404
from django.contrib.auth.models import User,auth ,Group
from django.http import Http404, HttpResponse
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.contrib import messages
from django.contrib.auth import authenticate,get_user_model
from django.contrib import auth 
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required,permission_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from . decorators import unauthenticated_user ,allowed_user ,admin_only
import datetime  
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import PageNotAnInteger,EmptyPage,Paginator
import os
from django.http import JsonResponse
from . forms import UserForm 
import requests
from django.db.models import Q
import json
from django.urls import reverse_lazy
from .models import Enquiry
import datetime
from django.core.paginator import PageNotAnInteger,EmptyPage,Paginator
from django.template.loader import render_to_string
from django.contrib import auth 



def login(request):
    return render(request,'html_files/login.htm')