from django.test import TestCase
from .models import Tickets
from django.test import client
import json
import requests
import datetime
import time
import _thread
import threading

def normalResearchTest(city,lock):
    """
    docstring
    """

    dict = {}
    dict['dcityName'] = city.get("dcityName")
    dict['acityName'] = city.get("acityName")
    dict['dtime'] = str(dtime)
    print(dict)

    response = requests.get(url=url,params=dict)
    r.acquire()
    if(response.status_code == 200):
        global success
        success += 1
    global total
    total += 1
    r.release()
    lock.release()
    pass

success = 0
total = 0
r = threading.Lock()
cities = open("cities4.json", "r", encoding="utf8")
cities = json.load(cities)
print(type(cities))
dtime = datetime.datetime.now().date()

url = "https://airaflyscanner.site:8080/normalResearch/"
i = 0
locks = []
for city in cities:
    lock = _thread.allocate_lock()
    lock.acquire()
    locks.append(lock)
    try:
        _thread.start_new_thread(normalResearchTest, (city, lock))
        i += 1
    except Exception as identifier:
        print(identifier)

    if (i > 100):
        break

for i in locks:
    while (i.locked()):
        pass

# Create your tests here.
