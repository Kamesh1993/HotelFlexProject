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
from app.forms import RegisterForm, LoginForm, RoomBooking, Reservation
from datetime import datetime
from app.models import UserDetails, RoomBooking
import mysql.connector
from passlib.hash import sha256_crypt
import pymysql

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

def booking(request):
    """Renders the booking page only after the user logs in"""
    if 'email' in request.session:
        return render(request,'app/booking.html')
    else:
        return HttpResponseRedirect('/login')

def roombooking(request):
    try:
        global room_details
        room_details = []
        if 'email' in request.session:
            if request.method=='POST':
                form = RoomBooking(request.POST)
                check_in = request.POST.get('checkin')
                cin = changeDateFormat(check_in)
                check_out = request.POST.get('checkout')
                cout = changeDateFormat(check_out)
                email = request.session['email']
                hotel_name = request.session['hotel']
                room = request.POST.get('rooms')
                room_details = [cin,cout,email,hotel_name,room]
                return render(request,'app/rooms.html')
        else:
            return render(request,'app/booking.html')
    except:
        return render(request,'app/index.html')

def single(request):
    #try:
    if 'email' in request.session:
        if request.method=='POST':
            form = Reservation(request.POST)
            firstname = form['firstname'].value()
            middlename = form['middlename'].value()
            lastname = form['lastname'].value()
            email = form['email'].value()
            phone = form['phone'].value()
            address = form['address'].value()
            city = form['city'].value()
            state = form['state'].value()
            zipcode = form['zipcode'].value()
            idproof = form['idproof'].value()
            rooms = form['rooms'].value() 
            details = [firstname,middlename,lastname,email,phone,address,city,state,zipcode,idproof,rooms]
            reservation('single',details)
            return render(request,'app/reservation.html')
        return render(request,'app/singlerooms.html')
    else:
        return render(request,'app/login.html')
    #except:
    return render(request,'app/booking.html')

def double(request):
    try:
        if 'email' in request.session:
            return render(request,'app/doublerooms.html')
        else:
            return render(request,'app/login.html')
    except:
        return render(request,'app/booking.html')

def luxury(request):
    try:
        if 'email' in request.session:
            return render(request,'app/singlerooms.html')
        else:
            return render(request,'app/login.html')
    except:
        return render(request,'app/booking.html')

def reservation(room,details):
    today_date = int(datetime.now().strftime("%Y%m%d%H%M%S"))
    rb = RoomBooking(today_date,room_details[0],room_details[1],details[0],details[1],details[2],details[3],details[4],details[5],details[6],details[7],details[8],details[9],details[10])
    rb.save()
    user = User.objects.get(email=room_details[2])
    conn = pymysql.connect(host= "localhost",user="root",passwd="superstar007",db="hotelflexproject")
    cur = conn.cursor()
    cur.execute("""INSERT INTO reservation VALUES (%s,%s,%s,%s,%s)""",(today_date,room_details[0],room_details[1],details[3],user.id))
    conn.commit()

def changeDateFormat(date):
    d_list = date.split('/')
    modified_date = d_list[2]+'-'+d_list[0]+'-'+d_list[1]
    return modified_date
