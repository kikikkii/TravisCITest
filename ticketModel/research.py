
import requests
import json
import datetime 
from datetime import timedelta 
from fake_useragent import UserAgent
import time
import random
from ticketModel.ticketSerializer import Ticket2Serializer,companyTicket
import execjs
import _thread
import importlib

def gen_dates(start_date,day_counts):
    next_day = timedelta(days=1)  # timedalte 是datetime中的一个对象，该对象表示两个时间的差值,day=1表示相差一天 
    for i in range(day_counts): # 从起始时间的现在 
        yield start_date + next_day * i 


def get_date_list(start_date): 
    """ 
    :param start_date: 开始时间 
    :return: 开始时间未来40天后的日期列表 
    """
    start = start_date
    end = start + datetime.timedelta(days=1) # 爬取未来一个月的机票
    data = [] 
    for d in gen_dates(start, ((end - start).days)): 
        data.append(d.strftime("%Y-%m-%d")) 
    return data 

def getcities(cityName):
    with open("cities4.json","r",encoding="utf8") as f:
        cities_data = json.load(f)
        cities_list = []
        for i in cities_data:
            if i['dcityName'] == cityName:
                cities_list.append(i)
        return cities_list

def getcity(cityName):
    with open("cities.json","r",encoding='utf8') as file:
        cities = json.load(file)
        for i in cities:
            if i['name'] == cityName:
                return i['code']

def js_from_file(file_name):
    with open(file_name, 'r', encoding='UTF-8') as file:
        result = file.read()
    return result

def getDirectResearch(cityName,dtime):
    start_date = datetime.datetime.strptime(dtime, "%Y-%m-%d") # <class 'datetime.datetime'>
    date_data = get_date_list(start_date)
    cities_data = getcities(cityName)
    print(cities_data)
    print(date_data)
    FlightList = []
    for day in date_data: 
        for city_data in cities_data:
            dcity = city_data.get('dcity')
            acity = city_data.get('acity')
            dcityName = city_data.get('dcityName')
            acityName = city_data.get('acityName')
            try:
                _thread.start_new_thread(getNormalResearch,(dcity,acity,dcityName,acityName,day))
            except Exception as e:
                print(e)
            time.sleep(0.1)
    return FlightList

def getNormalResearch(dcity,acity,dcityName,acityName,dtime):
    # 这里的url 必须写全！！！不能只写个path


    url = "https://flights.ctrip.com/itinerary/api/12808/products/oneway/{}-{}?date={}".format(dcity,
                                                                                               acity,
                                                                                               dtime)
    print(url)
    headers = {
        'User-Agent': '{}'.format(UserAgent().random),
        'Referer': 'https://flights.ctrip.com/itinerary/oneway/{}-{}?date={}'.format(dcity, acity, dtime),
        "Content-Type": "application/json"
    }
    context1 = execjs.compile(js_from_file('test.js'))
    token = context1.call("get_token", dcity, acity, "Oneway")
    request_payload = {
        "flightWay": "Oneway",
        "classType": "ALL",
        "hasChild": False,
        "hasBaby": False,
        "searchIndex": 1,
        "airportParams": [
            {"dcity": "{}".format(dcity),
             "acity": "{}".format(acity),
             "dcityname": "{}".format(dcityName),
             "acityname": "{}".format(acityName),
             "date": "{}".format(dtime),
             }
        ],

        "token": token
    }
    # post请求
    response = requests.post(url, data=json.dumps(request_payload), headers=headers, timeout=30).text
    # print(response)
    # json.dumps 将 Python 对象编码成 JSON 字符串
    routeList = json.loads(response).get('data').get('routeList')  # 字典 get('key') 返回 value
    if (routeList == None):
        print("There is None")
        # continue
        return
    # json.loads 将已编码的 JSON 字符串解码为 Python 对象
    # 依次读取每条信
    for route in routeList:
        # 不是直达的机票就跳过
        if (route['routeType'] != 'Flight'):
            # continue
            return
        dict = {}
        if len(route.get('legs')) >= 1:
            legs = route.get('legs')
            flight = legs[0].get('flight')
            """
            提取想要的信息 
            """
            if (flight == None):
                continue

            dict['flightNumber'] = flight.get('flightNumber')
            dict['companyName'] = flight.get('airlineName')

            dict['dcity'] = flight.get('departureAirportInfo').get('cityTlc')
            dict['dcityName'] = flight.get('departureAirportInfo').get('cityName')
            dict['departureDate'] = flight.get('departureDate')
            dict['dairport'] = flight.get('departureAirportInfo').get('airportName')

            dict['acity'] = flight.get('arrivalAirportInfo').get('cityTlc')
            dict['acityName'] = flight.get('arrivalAirportInfo').get('cityName')
            dict['arrivalDate'] = flight.get('arrivalDate')
            dict['aairport'] = flight.get('arrivalAirportInfo').get('airportName')

            cabins = legs[0].get('cabins')
            cabin = cabins[0]
            dict['price'] = cabin.get('price').get('price')
            dict['rate'] = cabin.get('price').get('rate')
            dict['url'] = 'https://www.ctrip.com/'
            ticket = Ticket2Serializer(data=dict)
            ticket.is_valid()
            ticket.save()
            time.sleep(0.01)

def getCompanyTicket(companyName):
    company = importlib.import_module('companyTicket.' + companyName)
    list = company.getTickets()
    for i in list:
        print(i)
    return list