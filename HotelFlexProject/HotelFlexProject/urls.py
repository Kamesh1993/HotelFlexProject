"""
Definition of urls for HotelFlexProject.
"""

from datetime import datetime
from django.urls import path
import django.contrib.auth.views

import app.forms
import app.views

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    path('', app.views.home, name='home'),
    path('contact', app.views.contact, name='contact'),
    path('about', app.views.about, name='about'),
    path('register/',app.views.register,name='register'),
    path('login/',app.views.login,name='login'),
    path('booking/',app.views.booking,name='booking'),
    path('logout',app.views.logout,name='logout'),
    path('roombooking/',app.views.roombooking,name='roombooking'),
    path('reserve/<str:roomtype>',app.views.reserve,name='roombooking'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
]
