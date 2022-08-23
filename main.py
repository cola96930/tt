from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
import http.client, urllib
import json


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


def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def lizhi():
    conn = http.client.HTTPSConnection('api.tianapi.com')  #接口域名
    params = urllib.parse.urlencode({'key':'a59bb78a1149fb897531644c84f7d262'})
    headers = {'Content-type':'application/x-www-form-urlencoded'}
    conn.request('POST','/lzmy/index',params,headers)
    res = conn.getresponse()
    data = res.read()
    data = json.loads(data)
    return data["newslist"][0]["saying"]

def kqzl():
    conn = http.client.HTTPSConnection('api.tianapi.com')  #接口域名
    params = urllib.parse.urlencode({'key':'a59bb78a1149fb897531644c84f7d262','area':'上海'})
    headers = {'Content-type':'application/x-www-form-urlencoded'}
    conn.request('POST','/aqi/index',params,headers)
    res = conn.getresponse()
    data = res.read()
    return data["newslist"][0]["quality"]
  
def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"lizhi":{"value":lizhi()},"kqzl":{"value":kqzl()},"birthday_left":{"value":get_birthday()},"tbirthday_left":{"value":get_tbirthday()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
