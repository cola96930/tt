from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']
tbirthday = os.environ['TBIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_tbirthday():
  next = datetime.strptime(str(date.today().year) + "-" + tbirthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def tip():
    if (tianqi_API!="否"):
        conn = http.client.HTTPSConnection('api.tianapi.com')  #接口域名
        params = urllib.parse.urlencode({'key':tianqi_API,'city':city})
        headers = {'Content-type':'application/x-www-form-urlencoded'}
        conn.request('POST','/tianqi/index',params,headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data)
        pop = data["newslist"][0]["pop"]
        tips = data["newslist"][0]["tips"]
        return pop,tips
    else:
        return "",""

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"weather":{"value":wea},"temperature":{"value":temperature},"tips":{"value":tip},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"tbirthday_left":{"value":get_tbirthday()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
pop,tips = tip()
print(res)
