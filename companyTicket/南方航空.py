import requests
import json
def getTickets():
    url= 'https://b2c.csair.com/portal/minPrice/queryMinPriceInAirLines?jsoncallback=getMinPrice&inter=N&callback=getMinPrice&_=1607846317154'
    reponse = requests.get(url=url).text
    reponse = reponse[12:-1]
    # print(reponse)
    data = json.loads(reponse)
    flights= data.get("FROMOFLIGHTS")
    list = []
    for flight in flights:
        dict = {}
        dict['dcityName'] = flight.get('DEPCTIYNAME_ZH')
        tickets = flight.get("FLIGHT")
        for ticket in tickets:
            dict['acityName'] = ticket.get('ARRCTIYNAME_ZH')
            dict['price'] = ticket.get('MINPRICE')
            dict['companyName']  = '南方航空'
            print(dict)
            if dict not in list:
                list.append(dict)
    return list