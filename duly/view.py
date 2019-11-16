from django.shortcuts import render
from django.http import *
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.urls import reverse, reverse_lazy
from django.db.models import Count
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import os
from django.http import HttpResponse
from .scheduler import scheduler

def myfunc():
    print ("DONE")

job = scheduler.add_job(myfunc, 'interval', minutes=1)




def user_registration(request):   
    return render(request, 'registration.html', {}) 

@login_required(login_url=reverse_lazy('login'))
def home_view(request):
    return render(request, 'home.html', {})   

@login_required(login_url=reverse_lazy('login'))
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))
