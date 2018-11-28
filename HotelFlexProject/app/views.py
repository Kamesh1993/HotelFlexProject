from django.shortcuts import render
from django.conf import settings
from django.http import HttpRequest, HttpResponseRedirect
from django.contrib.messages import warning
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages,auth
from app.forms import RegisterForm, LoginForm, RoomBooking
from datetime import datetime
from app.models import UserDetails
import mysql.connector
from passlib.hash import sha256_crypt

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(request,'app/index.html')

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(request,'app/contact.html')

def about(request):
    """Renders the about page."""
    return render(request,'app/about.html')

def register(request):
    """Renders the register page."""
    try:
        assert isinstance(request, HttpRequest)
        if request.method=='POST':
            form = RegisterForm(request.POST)
            if(form.is_valid()):
                firstname = form['firstname'].value()
                lastname = form['lastname'].value()
                email = form['email'].value()
                address = form['address'].value()
                password = sha256_crypt.encrypt(form['password'].value())
                user_auth = User.objects.create_user(username=email,first_name=firstname,last_name=lastname,email=email,password=password)
                user = UserDetails(email,address,password)
                user_auth.save()
                user.save()
                return render(request,'app/login.html')
        else:
            form = RegisterForm()
        return render(request,'app/register.html',{'form':form})
    except:
        return render(request,'app/index.html')

def login(request):
    """Renders the login page"""
    try:
        assert isinstance(request, HttpRequest)
        if 'email' in request.session:
            return HttpResponseRedirect('/booking')
        elif request.method=='POST':
            form = LoginForm(request.POST)
            if(form.is_valid()):
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                login_cred=UserDetails.objects.filter(email=email).values()
                details = login_cred[0]
                if email==details['email'] and sha256_crypt.verify(password,details['password']):
                    if 'email' not in request.session:
                        request.session['email']=email
                        request.session['hotel']='Royal Grand'
                    return HttpResponseRedirect('/booking')
                else:
                    messages.warning(request,'Invalid email/password, Please try again!')
                    return render(request,'app/login.html')
        else:
            form = LoginForm()
        return render(request,'app/login.html')
    except:
        return render(request,'app/index.html')

def logout(request):
    users = User.objects.get(email=request.session['email'])
    users.is_active=False
    users.save()
    del(request.session['email'])
    return HttpResponseRedirect('/')
