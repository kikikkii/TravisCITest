from rest_framework import serializers
from .models import Wxuser,concernFlight
from ticketModel.ticketSerializer import Ticket2Serializer
from ticketModel.models import Tickets
import sys
sys.path.append("..")
from ticketModel.ticketSerializer import Ticket2Serializer

class WxuserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wxuser
        fields = '__all__'

class concernFlightSerializer(serializers.ModelSerializer):
    ticketDetail = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = concernFlight
        fields = '__all__'

    # ticketsSerializer = Ticket2Serializer
    # WxuserSerializer = WxuserSerializer

    def get_ticketDetail(self,obj):
        print(obj.ticketId)
        return Ticket2Serializer(instance=obj.ticketId).data
        # print(t)