from django.shortcuts import render
from . import models, sendMessage
from . import ticketSerializer, airplaneSerializer
from django.core import serializers
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from django.db.models import Min, Count, F, Avg
import json
from .research import *
from userInfo.models import concernFlight,Wxuser


class directResearch(APIView):
    def get(self, request):
        sortType = request.GET.get('sortType')
        dcityName = request.GET.get('dcityName')
        dtime = request.GET.get('dtime')
        # dcityName = '上海'
        # dtime = '2020-12-12'
        if (sortType == 'price'):
            query_list = models.Tickets.objects.filter(dcityName=dcityName, departureDate__date=dtime).order_by('price')
        elif (sortType == 'time'):
            query_list = models.Tickets.objects.filter(dcityName=dcityName, departureDate__date=dtime).order_by('departureDate')
        elif (sortType == 'rate'):
            query_list = models.Tickets.objects.filter(dcityName=dcityName, departureDate__date=dtime).order_by('rate')
        else:
            query_list = models.Tickets.objects.filter(dcityName=dcityName, departureDate__date=dtime)

        if(len(query_list)>0):
            pass
        else:
            FlightLists = getDirectResearch(dcityName,dtime)
            # serializer = ticketSerializer.Ticket2Serializer(data=FlightLists,many=True)
            print(dict)
            # if serializer.is_valid(raise_exception=True):
            #     print("*************************")
                # serializer.save()
            # process = CrawlerProcess(get_project_settings())
            # process.crawl(CtripSpider, {'REQUEST_ENABLED':True,'dcity':'福州', 'date':'2020-12-28'})
        query_list = models.Tickets.objects.filter(dcityName=dcityName, departureDate__date=dtime)
        query_list2 = query_list.values('acity').annotate(tmin=Min('price'))
        allcities = []
        list = []
        for i in query_list2:
            for j in query_list:
                if j.price == i['tmin'] and j.acity == i['acity'] and j.acity not in allcities:
                    allcities.append(j.acity)
                    list.append(j)
        serializer = ticketSerializer.Ticket2Serializer(list, many=True)
        return JsonResponse(serializer.data, safe=False)

class NormalResearch(APIView):
    def get(self, request):
        print(request.GET)
        sortType = request.GET.get('sortType')
        dcityName = request.GET.get('dcityName')
        dtime = request.GET.get('dtime')
        acityName = request.GET.get('acityName')
        dtime2 = request.GET.get('dtime2')
        # dcityName = '福州'
        # acityName = '北京'
        # dtime = '2020-12-21'
        print(dcityName)
        if (sortType == 'price'):
            query_list = models.Tickets.objects.filter(acityName=acityName, dcityName=dcityName, departureDate__date=dtime).order_by('price')
        elif (sortType == 'time'):
            query_list = models.Tickets.objects.filter(acityName=acityName, dcityName=dcityName, departureDate__date=dtime).order_by('departureDate')
        elif (sortType == 'rate'):
            query_list = models.Tickets.objects.filter(acityName=acityName, dcityName=dcityName, departureDate__date=dtime).order_by('rate')
        else:
            query_list = models.Tickets.objects.filter(acityName=acityName, dcityName=dcityName, departureDate__date=dtime)

        if len(query_list) <= 0:
            dcity = getcity(dcityName)
            acity = getcity(acityName)
            getNormalResearch(dcity, acity, dcityName, acityName, dtime)
            # serializer = ticketSerializer.Ticket2Serializer(data=FlightLists, many=True)
        query_list = models.Tickets.objects.filter(dcityName=dcityName, acityName=acityName, departureDate__date=dtime)
        if dtime2:
            query_list2 = models.Tickets.objects.filter(dcityName=dcityName, acityName=acityName,departrureDate__date=dtime2)
            if(len(query_list2) < 0):
                dcity = getcity(dcityName)
                acity = getcity(acityName)
                getNormalResearch(dcity, acity, dcityName, acityName, dtime2)
            query_list2 = models.Tickets.objects.filter(dcityName=dcityName, acityName=acityName,departrureDate__date=dtime2)
            # for flight in query_list:
                # flight.price = flight +

        serializer = ticketSerializer.Ticket2Serializer(query_list,many=True)
        return JsonResponse(serializer.data,safe=False)

    def post(self, request):
        print('************')
        dict = request.data
        print(type(dict))
        #dict = json.loads(postdata)
        dcity = dict.get('dcity')
        #print(dcity)
        acity = dict.get('acity')
        #print(acity)
        dtime = dict.get('departureDate')
        #print(dtime)
        flightNumber = dict.get('flightNumber')
        query = models.Tickets.objects.filter(dcity=dcity,acity=acity,departureDate=dtime,flightNumber=flightNumber)
        print(query.values())
        print("*******************")
        if query.count() != 0:
            for i in query:
                # if i.price >= int(dict['price']):
                #     return HttpResponse('已有数据')
                # else:
                i.url = dict['url']
                i.rate = dict['rate']
                i.price = dict['price']
                i.companyName = dict['companyName']
                i.save()
                print(i.id)
                query2 = concernFlight.objects.filter(ticketId = i.id)
                print(query2.values())
                for j in query2:
                    sendMessage.sendMessage(j.openid_id,j.orgPrice,i.price)
                return HttpResponse('更新成功')

        serializer = ticketSerializer.Ticket2Serializer(data=dict)
        print(dict)
        if serializer.is_valid(raise_exception=True):
            print("*************************")
            serializer.save()
            return HttpResponse("OK")

class updateTicket(APIView):
    def post(self,request):
        print("this is update")
        dict = request.data
        #确定机票的航线没有重复
        ddata = dict.get('ddate') #出发日期
        dcityName = dict.get('dcityName') #出发城市
        acityName = dict.get('acityName') #到达城市
        if airplaneSerializer.airplaneSerializer.is_valid(dict):
            serializer = airplaneSerializer.airplaneSerializer(data=dict)
        serializer.save()
        print('保存成功')

class getcities(APIView):
    def get(self,request):
        list = []
        dcityName = request.GET.get('dcityName')
        departureDate = request.GET.get('dtime')
        print("test1")
        query = models.Tickets.objects.filter(dcityName=dcityName, departureDate__date=departureDate)
        print("test2")
        for city in query:
            dict = {
                'acity':city.acity,
                'dcity':city.dcity,
                'acityName':city.acityName,
                'dcityName':city.dcityName
            }
            if dict not in list:
                list.append(dict)
        return JsonResponse(list,safe=False)

class companyTickets(APIView):
    def get(self,request):
        companyName = request.GET.get('companyName')
        print(companyName)
        date = datetime.date.today()
        print(date)
        query = companyTicket.objects.filter(companyName=companyName,saveDate=str(date))
        print(query)
        if query:
            list = ticketSerializer.companyTicketSerializer(instance=query, many=True)
            return JsonResponse(list.data,safe=False)
        list = getCompanyTicket(companyName)
        print(list)
        serializer = ticketSerializer.companyTicketSerializer(data=list,many=True)
        serializer.is_valid()
        serializer.save()
        return JsonResponse(serializer.data,safe=False)

#  Create your views here.