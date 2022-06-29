from cgitb import text
from multiprocessing import context
from operator import index
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

#from config import *


def get_tencent_data():
    header = {
        'User-Agent':
        r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'
    }
    # url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    url1 = 'https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=diseaseh5Shelf'
    # url2 = 'https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=chinaDayList,chinaDayAddList'
    url2 = 'https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=chinaDayList,chinaDayAddList,cityStatis,provinceCompare'
    res = requests.get(url1, headers=header).json()
    res2 = requests.get(url2, headers=header).json()

    data = res['data']['diseaseh5Shelf']
    data2 = res2['data']
    del data2["chinaDayAddList"][0]
    del data2["chinaDayAddList"][0]
    print(data2["chinaDayAddList"][0])
    # data3 = data2["chinaDayAddList"]
    """ 
    
    del  data3[0]
    data4= data3 """

    history = {}  # 历史数据
    for i in data2["chinaDayList"]:
        ds = i["y"] + "." + i["date"]
        tup = time.strptime(ds, "%Y.%m.%d")
        ds = time.strftime("%Y-%m-%d", tup)  # 改变时间格式,不然插入数据库会报错，数据库是datetime类型

        # 本土现有确诊
        localConfirmH5 = i["localConfirmH5"]
        # 现有确诊
        nowConfirm = i["nowConfirm"]
        # 累计确诊
        confirm = i["confirm"]
        # 无症状感染
        noInfect = i["noInfect"]
        # 输入性病例
        importedCase = i["importedCase"]
        # 累计死亡
        dead = i["dead"]
        # 现有疑似
        suspect = i["suspect"]
        # 累计治愈
        heal = i["heal"]
        # 现有重症
        nowSevere = i["nowSevere"]

        history[ds] = {
            "localConfirmH5": localConfirmH5,
            "nowConfirm": nowConfirm,
            "confirm": confirm,
            "noInfect": noInfect,
            "importedCase": importedCase,
            "dead": dead,
            "suspect": suspect,
            "heal": heal,
            "nowSevere": nowSevere
        }
    for i in data2["chinaDayAddList"]:

        ds = i["y"] + "." + i["date"]
        tup = time.strptime(ds, "%Y.%m.%d")
        ds = time.strftime("%Y-%m-%d", tup)
        # 新增确诊
        confirm = i["confirm"]
        # 新增疑似
        suspect = i["suspect"]
        # 新增治愈
        heal = i["heal"]
        # 新增死亡
        dead = i["dead"]
        # 新增本土确诊
        localConfirmadd = i["localConfirmadd"]
        # 新增境外
        importedCase = i["importedCase"]
        # 新增疑似
        infect = i["infect"]
        # 删除字典第一个冲突项

        history[ds].update({
            "confirm_add": confirm,
            "suspect_add": suspect,
            "heal_add": heal,
            "dead_add": dead,
            "localConfirm_add": localConfirmadd,
            "importedCase_add": importedCase,
            "noInfect_add": infect
        })

    details = []
    update_time = data['lastUpdateTime']
    data_province = data['areaTree'][0]['children']
    for pro_infos in data_province:
        province = pro_infos['name']
        for city_infos in pro_infos['children']:
            city = city_infos['name']
            confirm = city_infos['total']['confirm']
            confirm_add = city_infos['today']['confirm']

            heal = city_infos['total']['heal']
            dead = city_infos['total']['dead']
            nowConfirm = city_infos['total']['nowConfirm']
            details.append([
                update_time, province, city, confirm, confirm_add, heal, dead,
                nowConfirm
            ])
    return {"history": history, "details": details}


def insert_history(data: dict):
    try:
        print(f'{time.asctime()} 开始插入数据')
        cursor = db.cursor()
        for k, v in data.items():
            sql_query = f"insert into history values('{k}',{v['localConfirmH5']},{v['nowConfirm']}," \
                        f"{v['importedCase']},{v['importedCase_add']},"\
                        f"{v['confirm']},{v['confirm_add']},{v['noInfect']},{v['noInfect_add']},"\
                        f"{v['suspect']},{v['suspect_add']},{v['heal']},{v['heal_add']}," \
                        f"{v['dead']},{v['dead_add']},{v['nowSevere']})"
            print(sql_query)
            cursor.execute(sql_query)
        db.commit()
        print(f'{time.asctime()} 完成插入数据')
    except:
        traceback.print_exc()
    finally:
        cursor.close()


def update_history(data: dict):
    # print(data)
    try:
        print(f'{time.asctime()} 开始更新历史数据')
        cursor = db.cursor()
        sql = "insert into history values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        sql_query = 'select confirm from history where ds=%s'
        for k, v in data.items():
            if not cursor.execute(sql_query, k):
                cursor.execute(sql, [
                    k,
                    v.get('localConfirmH5'),
                    v.get('nowConfirm'),
                    v.get('importedCase'),
                    v.get('importedCase_add'),
                    v.get('confirm'),
                    v.get('confirm_add'),
                    v.get('noInfect'),
                    v.get('noInfect_add'),
                    v.get('suspect'),
                    v.get('suspect_add'),
                    v.get('heal'),
                    v.get('heal_add'),
                    v.get('dead'),
                    v.get('dead_add'),
                    v.get('nowSevere'),
                    v.get('localConfirm_add')
                ])
        db.commit()
        # print(data)---+
        print(f'{time.asctime()} 完成更新历史数据')
    except:
        traceback.print_exc()
    finally:
        if 'cursor' in locals().keys():
            cursor.close()


def update_details(data: list):
    cursor = None
    try:
        cursor = db.cursor()
        # 子查询，选中update_time字段，按照id字段的降序排列顺序，选出update_time字段第一个
        # 将返回的时间与我们传入的时间比较，相同返回1
        sql = 'select %s=(select update_time from details order by id desc limit 1)'
        # 指定插入顺序
        sql_query = f"insert into details (update_time,province,city,confirm,confirm_add," \
                    f"heal,dead,nowConfirm) values(%s,%s,%s,%s,%s,%s,%s,%s)"
        print(data[0][0])
        cursor.execute(sql, data[0][0])  #对比最大时间戳
        result = cursor.fetchone()[0]
        if not result:
            print(f'{time.asctime()} 开始更新details数据')
            for item in data:
                # print(item)
                cursor.execute(sql_query, item)
            db.commit()
            print(f'{time.asctime()} 完成更新details数据')
        else:
            print(f'{time.asctime()} 已是最新details数据')
    except:
        traceback.print_exc()
    finally:
        if cursor:
            cursor.close()


# 国内时事热点
def get_baidu_news():
    url = r"https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_aladin_banner#tab1"  # 时事热点地址
    option = ChromeOptions()
    option.add_argument('--headless')
    option.add_argument("--no-sandbox")
    browser = Chrome(options=option)
    browser.get(url)

    but = browser.find_element_by_xpath('//*[@id="ptab-1"]/div[3]/div[11]')
    but.click()
    time.sleep(1)

    all = browser.find_elements_by_xpath(
        '//*[@id="ptab-1"]/div[3]/div/div[2]/a')

    context = [i.text for i in all]
    href = [i.get_attribute('href') for i in all]
    # print(href)
    date = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime())
    dates = []
    for i in range(len(context)):
        dates.append(date)

    # print(len(dates),len(context),dates,context)
    dc = zip(dates, context, href)
    pdf = pd.DataFrame(dc, columns=['data', 'content', 'href'])
    # pdf.to_sql(name=in, con=enging, if_exists="append")
    return pdf


def update_news(pdf):

    try:

        enging = create_engine(
            "mysql+pymysql://root:password@localhost:3306/covid")
        pdf.to_sql(name='hotsearch',
                   con=enging,
                   if_exists="append",
                   index=False)
    except:
        traceback.print_exc()
        print('出错了')


db = pymysql.connect(host="127.0.0.1",
                     user="root",
                     passwd="password",
                     database="covid")
data = get_tencent_data()
# insert_history(data['history'])
update_history(data['history'])
update_details(data['details'])
xx = get_baidu_news()
update_news(xx)

db.close()
