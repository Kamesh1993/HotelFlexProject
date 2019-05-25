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
from mysql.connector import Error
from mysql.connector import errorcode
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

def restaurant(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(request,'app/restaurant.html')

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
                det=User.objects.filter(email=email).values()
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
    try:
        users = User.objects.get(email=request.session['email'])
        users.is_active=False
        users.save()
        del(request.session['email'])
        return HttpResponseRedirect('/')
    except:
        return HttpResponseRedirect('/')

def booking(request):
    """Renders the booking page only after the user logs in"""
    try:
        if 'email' in request.session:
            return render(request,'app/booking.html')
        else:
            return HttpResponseRedirect('/login')
    except:
        return HttpResponseRedirect('/login')


def roombooking(request):
    try:
        global room_details, cin, cout
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
    try:
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
                name = firstname+" "+middlename+" "+lastname
                return render(request,'app/reservation.html',{'name':name,'room':rooms,'cin':cin,'cout':cout,'bid':today_date})
            return render(request,'app/singlerooms.html')
        else:
            return render(request,'app/login.html')
    except:
        return render(request,'app/booking.html')

def double(request):
    try:
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
                name = firstname+" "+middlename+" "+lastname
                return render(request,'app/reservation.html',{'name':name,'room':rooms,'cin':cin,'cout':cout,'bid':today_date})
            else:
                return render(request,'app/doublerooms.html')
        else:
            return render(request,'app/login.html')
    except:
        return render(request,'app/booking.html')

def deluxe(request):
    try:
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
                reservation('deluxe',details)
                name = firstname+" "+middlename+" "+lastname
                return render(request,'app/reservation.html',{'name':name,'room':rooms,'cin':cin,'cout':cout,'bid':today_date})
        else:
            return render(request,'app/login.html')
    except:
        return render(request,'app/booking.html')

def luxury(request):
    try:
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
                name = firstname+" "+middlename+" "+lastname
                return render(request,'app/reservation.html',{'name':name,'room':rooms,'cin':cin,'cout':cout,'bid':today_date})
        else:
            return render(request,'app/login.html')
    except:
        return render(request,'app/booking.html')

def executive(request):
    try:
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
                name = firstname+" "+middlename+" "+lastname
                return render(request,'app/reservation.html',{'name':name,'room':rooms,'cin':cin,'cout':cout,'bid':today_date})
        else:
            return render(request,'app/login.html')
    except:
        return render(request,'app/booking.html')

def presidential(request):
    try:
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
                name = firstname+" "+middlename+" "+lastname
                return render(request,'app/reservation.html',{'name':name,'room':rooms,'cin':cin,'cout':cout,'bid':today_date})
            else:
                return render(request,'app/presidential.html')
        else:
            return render(request,'app/login.html')
    except:
        return render(request,'app/booking.html')

def reservation(room,details):
    try:
        global today_date
        today_date = int(datetime.now().strftime("%Y%m%d%H%M%S"))
        rb = RoomBooking(today_date,room_details[0],room_details[1],details[0],details[1],details[2],details[3],details[4],details[5],details[6],details[7],details[8],details[9],details[10])
        rb.save()
        user = User.objects.get(email=room_details[2])
        arguments = [today_date,room_details[0],room_details[1],details[3],user.id]
        database_insert('reservation',arguments)
    except:
        return render(request,'app/booking.html')


def changeDateFormat(date):
    d_list = date.split('/')
    modified_date = d_list[2]+'-'+d_list[0]+'-'+d_list[1]
    return modified_date

def bookinghistory(request):
    try:
        connection = mysql.connector.connect(host= "localhost",user="root",passwd="superstar007",db="hotelflexproject")
        cur = connection.cursor()
        stmt=User.objects.filter(email=request.session['email'])
        query = "select booking_id, check_in, check_out from "+table_name+" where user_id="+uid
        return render(request,'app/booking_history.html')
    except:
        return render(request,'app/booking.html')

def database_insert(table_name,args):
    try:
        connection = mysql.connector.connect(host= "localhost",user="root",passwd="superstar007",db="hotelflexproject")
        cur = connection.cursor()
        arguments = []
        length=len(args)
        for i in range(length):
            arguments.append('%s')
        arg = ''.join(arguments)
        st = str(arguments)
        st = st.replace("'","")
        st = st.replace("[","")
        st = st.replace("]","")
        ar = tuple(st)
        query = "insert into "+table_name+" values "+"("+st+")"
        cur.execute(query,args)
        connection.commit()
    except:
        connection.rollback()
    finally:
        if(connection.is_connected()):
            connection.close()

def forgotpassword(request):
    try:
        if request.method=='POST':
            fromaddr = 'ruby.coders@gmail.com'
            toaddrs  = request.form['email']
            msg = 'Your password is - P@$Sw0rd, please reset it.'
            username = 'ruby.coders@gmail.com'
            password = '$uperSt@r007'
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            server.login(username,password)
            server.sendmail(fromaddr, toaddrs, msg)
            server.quit()
            data = Register_db.query.filter_by(email=toaddrs).first()
            data.password = sha256_crypt.encrypt("P@$Sw0rd")
            db.session.commit()
            return redirect(url_for('login'))
        else:
            return render_template('ForgotPassword.html')
    except:
        return render_template('ForgotPassword.html')
