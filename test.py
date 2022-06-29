from cgitb import text
from multiprocessing import context
from operator import index
from numpy import dsplit
import pandas as pd
import pymysql
from sqlalchemy import create_engine
import time
import traceback
import requests
import json
#from time import strftime
import time

from click import option
from selenium.webdriver import Chrome, ChromeOptions

conn = pymysql.connect(host='127.0.0.1',
                       user='root',
                       password='password',
                       db='covid',
                       charset='utf8')
cursor = conn.cursor()
# 各地级市详情
provinceName = [
    '台湾', '上海', '香港', '北京', '四川', '河南', '天津', '福建', '吉林', '广东', '云南', '浙江',
    '青海', '山东', '辽宁', '广西', '江苏', '河北', '湖南', '贵州', '黑龙江', '江西', '山西', '内蒙古',
    '陕西', '甘肃', '湖北', '海南', '澳门', '新疆', '安徽', '宁夏', '西藏', '重庆'
]
sql1 = 'SELECT * FROM (select city,confirm_add,confirm,heal,dead as de from details where update_time=(select update_time from details order by update_time desc limit 1) and province=\"'
sql2 = '\" and update_time=(select update_time from details order by update_time desc limit 1) group by update_time) as a ORDER BY de DESC'
city = '香港'
sql3 = sql1 + city + sql2

cursor.execute(sql3)
data2 = cursor.fetchall()
print(data2)
print(sql1 + city + sql2)
print('\"')
""" sql = 'select * from (select * from details where province="上海" and update_time=(select update_time from details ' \
        'order by update_time desc limit 1)' \
        'group by city) as a ' \
        'ORDER BY de DESC' """

# 'SELECT * FROM ' \
#           '(select sum(nowConfirm),sum(confirm_add),sum(confirm),sum(heal),sum(dead) as de from details  ' \
#           'where update_time=(select update_time from details ' \
#           'order by update_time desc limit 1) and province="北京" ' \
#           'group by province) as a ' \
#           'ORDER BY de DESC'

# sql = 'SELECT * FROM ' \
#           '(select sum(nowConfirm),sum(confirm_add),sum(confirm),sum(heal),sum(dead) as de from details  ' \
#           'where update_time=(select update_time from details ' \
#           'order by update_time desc limit 1) and province="北京" ' \
#           'group by province) as a ' \
#           'ORDER BY de DESC'
#     cur.execute(sql)
#     data1 = cur.fetchall()[0]
#     # 各地级市详情
#     sql1 = 'SELECT * FROM (select city,confirm_add,confirm,heal,dead as de from details where update_time=(select update_time from details order by update_time desc limit 1) and province=\"'
#  '\" group by city) as a ORDER BY de DESC'
#     cur.execute(sql1)
#     data2 = cur.fetchall()
#     return render_template('common.html',data1=data1,data2=data2)
header = {
    'User-Agent':
    r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'
}
url1 = 'https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=VaccineSituationData'

res1 = requests.get(url1, headers=header).json()
data1 = res1['data']['VaccineSituationData']
for i in data1:
    # ds = i['y']+'.'+i['date']
    country = i['country']
    date = i['date']
    vaccinations = i['vaccinations']
    total = i['total_vaccinations']
    perHundred = i['total_vaccinations_per_hundred']
    vacDatas = {
        "country": country,
        "date": date,
        "total": total,
        "perHundred": perHundred
    }

    print(vacDatas)

url2 = 'https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=FAutoforeignList'
res2 = requests.get(url2, headers=header).json()
data2 = res2['data']['FAutoforeignList']
worldData = {}
for i in data2:
    ds = i["y"] + "." + i["date"]
    tup = time.strptime(ds, "%Y.%m.%d")
    ds = time.strftime("%Y-%m-%d", tup)
    country = i['name']
    confirm = i['confirm']
    dead = i['dead']
    heal = i['heal']
    nowConfirm = i['nowConfirm']
    worldData[ds] = {
        "country": country,
        "confirm": confirm,
        "dead": dead,
        "heal": heal,
        "nowConfirm": nowConfirm
    }

    print(worldData)