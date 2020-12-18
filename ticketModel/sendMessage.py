from userInfo import models
import json
import requests
import datetime

def getaccess_token():
    url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wxedc59eba48154310&secret=2a8f0e5712f828b24d037e78d2b43a74"
    response = requests.get(url=url, data=dict).text
    data = json.loads(response)
    return data.get('access_token')


def sendMessage(openid,orgPrice,nowPrice):
    print("this is sendMessage" + openid)
    openid = "o4BXH5AWYn5WoEfls622G-mTymkc"
    query = models.Wxuser.objects.filter(openid = openid).first()
    print(query)


    print(dict)

    url = 'https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token={}'.format(dict['access_token'])
    dict['access_token'] = getaccess_token()
    dict['touser'] = openid
    dict['template_id'] = 'lu4TyPHCeQvJPCSH-IJ9X1mL3jLQVTCODK50VffU1oI'
    dict['data'] = {
        'thing2': {
            'value': '您关注的机票价格变动了'
        },
        'time5': {
            'value': datetime.datetime.strptime(datetime.datetime.now(), "%Y-%m-%d")
        },
        'amount3': {
            'value': "100"
        },
        'amount4': {
            'value': '180'
        },
    }

    response2 = requests.post(url=url, data=json.dumps(dict)).text
    print(response2)

