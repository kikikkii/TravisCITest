from rest_framework import serializers
from .models import Tickets,companyTicket


class Ticket2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Tickets
        fields = '__all__'

class companyTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = companyTicket
        fields = ['dcityName','acityName','price','saveDate','companyName']