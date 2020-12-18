from django.db import models
from .Airplane import *

class Tickets(models.Model):
    departureDate = models.DateTimeField(auto_now=False,null=True)
    arrivalDate = models.DateTimeField(auto_now=False,null=True)
    dairport = models.CharField(max_length=50,null=True)
    aairport = models.CharField(max_length=50,null=True)
    flightNumber = models.CharField(max_length=20)
    dcity = models.CharField(max_length=20)
    dcityName = models.CharField(max_length=20,null=True)
    acity = models.CharField(max_length=20)
    acityName = models.CharField(max_length=20,null=True)
    price = models.IntegerField(null=True)
    rate = models.FloatField(null=True)
    url = models.CharField(max_length=150)
    companyName = models.CharField(max_length=50,null=True)

class companyTicket(models.Model):
    dcityName = models.CharField(max_length=50,null=True)
    acityName = models.CharField(max_length=50,null=True)
    price = models.CharField(max_length=50,null=True)
    saveDate = models.DateField(auto_now=True)
    companyName = models.CharField(max_length=50,null=True)
# Create your models here.