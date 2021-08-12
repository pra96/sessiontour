from colorsys import ONE_THIRD
from operator import mod
from django.db import models
from django.test import client
from users.models import User

class GuideInfo(models.Model):
    GUIDE_TYPE = [('public', 'Public'), ('private', 'Private')]
    guide = models.OneToOneField(User, blank=False, on_delete=models.CASCADE)
    PRICE_TYPES = [('fix', 'Fix'), ('negotiable', 'Negotiable')]
    priceType = models.CharField(choices=PRICE_TYPES, max_length=11)
    fix_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    variable_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    description = models.TextField(max_length=500, default="", blank=True)
    destination = models.CharField(max_length=100, default="", blank=True)
    mobile_number = models.CharField(max_length=12, default="", blank=True)
    tourType = models.CharField(choices=GUIDE_TYPE, max_length=20 , default="")

class TourReservations(models.Model):
    TOUR_TYPES = [('bouldering','Bouldering'), ('hiking','Hiking'), ('rock art', 'Rock Art'), ('technical climbing', 'Technical Climbing')]
    TOUR_STYLE = [('public', 'Public'), ('private', 'Private')]
    
    first_name = models.CharField(max_length=30, default="" ,null=False)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    email_id = models.EmailField(blank=True, null=True)
    reservationId = models.BigAutoField(primary_key=True, auto_created=True, default=None)
    mobile_phone = models.CharField(max_length=12, default="", blank=True)
    tourDate = models.CharField(default="" , blank=True, max_length=50)
    meetTime = models.CharField(default="" , blank=True, max_length=50)
    tourType = models.CharField(choices=TOUR_TYPES, max_length=20)
    booked_by_user = models.BigIntegerField(blank=True, default=0)
    guide_assigned = models.BigIntegerField(blank=True, default=0)
    destination = models.CharField(max_length=100, null=False)
    tourStyle = models.CharField(choices=TOUR_STYLE, max_length=8)
    comments = models.TextField(max_length=300, default="", blank=True)
    isAccept = models.BooleanField(default=False)
    number_of_clients = models.IntegerField(default=1)

class Tours(models.Model):
    TOUR_TYPES = [('bouldering','Bouldering'), ('hiking','Hiking'), ('rock art', 'Rock Art'), ('technical climbing', 'Technical Climbing')]
    TOUR_STYLE = [('public', 'Public'), ('private', 'Private')]
    
    tourType = models.CharField(choices=TOUR_TYPES, max_length=20)
    tourStyle = models.CharField(choices=TOUR_STYLE, max_length=8)
    tourDescription = models.TextField(max_length=500, blank=True)
    tourId = models.IntegerField(default=False, blank=False)
    maxPersonAllowed = models.IntegerField(default=0)
    variableCost = models.DecimalField(max_digits=6, decimal_places=2, default=0)    
    fixedCost = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    isActive = models.BooleanField(default=True)


class GuideTourMapping(models.Model):
    TOUR_TYPES = [('bouldering','Bouldering'), ('hiking','Hiking'), ('rock art', 'Rock Art'), ('technical climbing', 'Technical Climbing')]
    TOUR_STYLE = [('public', 'Public'), ('private', 'Private')]

    guideTourId = models.BigAutoField(primary_key=True, auto_created=True, default=None)
    meetTime = models.CharField(default="" , blank=True, max_length=50)
    tourDate = models.CharField(default="" , blank=True, max_length=50)
    tourType = models.CharField(choices=TOUR_TYPES, max_length=20)
    tourStyle = models.CharField(choices=TOUR_STYLE, max_length=8)
    destination = models.CharField(max_length=100, default="", blank=True)
    guide = models.BigIntegerField(blank=True, default=0)
    clients = models.JSONField(default=dict, null=True)
    numberOfPersons = models.IntegerField(default=0)
