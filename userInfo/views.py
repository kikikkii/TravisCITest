from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse,JsonResponse
from . import wx_login
from django.core.cache import cache
import hashlib, time,json
from .models import Wxuser,concernFlight
from .serializers import *
import sys
sys.path.append("..")
from ticketModel.models import Tickets

class Login(APIView):

    def post(self, request):
        param = request.data
        if not param.get('code'):
             return Response({'status':1, "msg":"缺少参数"})
        else:
            code = param.get('code')
            user_data = wx_login.get_login_info(code)
            if user_data:
                val = user_data['session_key'] + "&" + user_data['openid']
                has_user = Wxuser.objects.filter(openid=user_data['openid']).first()
                if not has_user:
                    Wxuser.objects.create(openid=user_data['openid'])
                Wxuser.objects.update()
                return Response({
                    'status': 0,
                    'msg': 'ok',
                    'data': {'token': val},
                    'openid' : user_data['openid']
                })
            else:
                return Response({'status':2, 'msg': "无效的code"})

class concernList(APIView):
    def get(self,request):
        openid = request.GET.get("openid")
        # openid = "123456"
        # 测试用
        print(openid)
        query = concernFlight.objects.filter(openid=openid)
        list = []
        for i in query:
            t = concernFlightSerializer(instance=i)
            Tickets.objects.filter(id=i.id).values()
            # print(i.orgPrice)
            # print("t.data\t" + str(t.data))
            list.append(t.data)
        print(list)
        return JsonResponse(list,safe=False)
        serializer = Ticket2Serializer(list, many=True)
        print(serializer.data)
        return JsonResponse(serializer.data, safe=False)

    def post(self,request):
        # 从request中获取数据

        dict = request.data.copy()
        openid = dict['openid']
        #
        query = concernFlight.objects.filter(openid=openid)
        print(query)
        for i in query:

            if(int(dict['ticketId']) == i.ticketId_id):
                return HttpResponse("已收藏")
        '''
        data = {
            'openid':'XXX',
            'ticketId':1111
            'orgPrice':180
        }
        '''
        # dict['ticketId'] = Tickets.objects.filter(id = dict['ticketId']).first()
        print(dict)
        serializer = concernFlightSerializer(data=dict)
        serializer.is_valid(raise_exception=False)
        # print(serializer.data)
        serializer.save()
        # print(serializer.data)

        return HttpResponse("收藏成功")

    def delete(self, request):
        dict = request.data
        openid = dict['openid']
        ticketId = dict['ticketId']
        query = concernFlight.objects.filter(openid=openid,ticketId=ticketId).first()
        query.delete()
        return HttpResponse("已取消关注")




# Create your views here.
