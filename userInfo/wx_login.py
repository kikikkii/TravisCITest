
AppId="wxedc59eba48154310" # 写你自己的小程序的id

AppSecret="2a8f0e5712f828b24d037e78d2b43a74" # 写你自己的小程序的秘钥

code2Session="https://api.weixin.qq.com/sns/jscode2session?appid={}&secret={}&js_code={}&grant_type=authorization_code"

import requests

def get_login_info(code):
    code_url = code2Session.format(AppId, AppSecret, code)
    response = requests.get(code_url)
    json_response = response.json() # 把它变成json的字典
    if json_response.get("session_key"):
        return json_response
    else:
        return False