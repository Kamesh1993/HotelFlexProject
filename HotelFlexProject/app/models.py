from django.db import models

class UserDetails(models.Model):
    email = models.EmailField(max_length=100,primary_key=True)
    address = models.TextField(max_length=400)
    password = models.CharField(max_length=140, default='NULL')

    class Meta:
        db_table = 'user'

    def __str__(self):
        return u'%s %s'  % (self.email,self.address)

class RoomBooking(models.Model):
    bookingid = models.BigIntegerField(primary_key=True,default=0)
    checkin  = models.CharField(max_length=140,default='NULL')
    checkout = models.CharField(max_length=140,default='NULL') 
    firstname = models.CharField(max_length=140)
    middlename = models.CharField(max_length=140)
    lastname = models.CharField(max_length=140)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=10)
    address = models.TextField(max_length=400)
    city = models.CharField(max_length=140)
    state = models.CharField(max_length=140)
    zipcode = models.IntegerField()
    idproof = models.CharField(max_length=140)
    rooms = models.CharField(max_length=40)
    
    class Meta:
        db_table = 'roombooking'
