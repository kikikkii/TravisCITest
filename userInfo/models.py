from django.db import models
import sys
sys.path.append("..")
from ticketModel.models import Tickets

# Create your models here.
class Wxuser(models.Model):
    id = models.AutoField(primary_key=True)
    openid=models.CharField(max_length=255,unique=True)
    def __str__(self):
        return self.openid

class concernFlight(models.Model):
    openid = models.ForeignKey('Wxuser',on_delete=models.CASCADE,to_field="openid")
    ticketId = models.ForeignKey(to=Tickets,on_delete=models.CASCADE)
    orgPrice = models.IntegerField(null=True)