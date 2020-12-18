import requests
import json
import urllib.parse
url = "http://www.9air.com/shop/api/shopping/b2c/searchflight/?"

    #     """?language=zh_CN&currency=CNY&flightCondition=index:0;\
    #     depCode:CAN;arrCode:CGQ;depDate:2020-12-02;depCodeType:AIRPORT;\
    #     arrCodeType:AIRPORT;&channelNo=B2C&tripType=OW&adultCount=1\
    #    &childCount=0&infantCount=0"""

data = "language=zh_CN\
    &currency=CNY&flightCondition=index:0;depCode:CAN;arrCode:CGQ;depDate:2020-12-02;depCodeType:AIRPORT;arrCodeType:AIRPORT;\
    &channelNo=B2C&tripType=OW&groupIndicator=I&adultCount=1&childCount=0&infantCount=0&airlineCode=&directType=&cabinClass=&taxFee=&taxCurrency=&promotionCode="
headers = {
    'Accept':'',
    'Accept-Encoding':'',
    'Accept-Language':'',
    'Cache-Control':'',
    'Connection':'',

}
dict = {
    'language':'zh_CN',
    'currency':'CNY',
    'flightCondition':{
            'index':0,
            'depCode':'CAN',
            'arrCode':'CGQ',
            'depDate':'2020-12-02',
            'depCodeType':'AIRPORT',
            'arrCodeType':'AIRPORT',
    },
    'channelNO':'B2C',
    'tripType':'OW',
    'groupIndicator':'I',
    'adultCount':1,
    'childCount':0,
    'infantCount':0
}
t = urllib.parse.urlencode(dict)
# s = urllib.parse.unquote(data)
print(t)
# json.dumps(dict)

response = requests.get(url = url+t,data=dict,headers=headers).text
print(response)