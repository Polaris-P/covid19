import json
import mimetypes
from multiprocessing.sharedctypes import Value

from threading import local
# from time import strftime
from tkinter.ttk import LabeledScale
from turtle import up
from unicodedata import name
from xml.dom.minidom import TypeInfo
from click import confirm
from flask import Flask, jsonify, render_template

import pymysql
import jinja2
from requests import Response
from datetime import date, datetime

app = Flask(__name__)

conn = pymysql.connect(host='127.0.0.1',
                       user='root',
                       password='password',
                       db='covid',
                       charset='utf8')

cur = conn.cursor()


def get_conn():
    """
    :return: 连接，游标
    """
    # 创建连接
    conn = pymysql.connect(host="127.0.0.1",
                           user="root",
                           password="password",
                           db="covid",
                           charset="utf8")
    # 创建游标
    cursor = conn.cursor()  # 执行完毕返回的结果集默认以元组显示
    return conn, cursor


def close_conn(conn, cursor):
    cursor.close()
    conn.close()


def query(sql, *args):
    """
    封装通用查询
    :param sql:
    :param args:
    :return: 返回查询到的结果，((),(),)的形式
    """
    conn, cursor = get_conn()
    cursor.execute(sql, args)
    res = cursor.fetchall()
    close_conn(conn, cursor)
    return res


@app.route("/home")
def index():
    cur = conn.cursor()
    # 获取最新国内数据
    # 新增
    dt1 = 'SELECT confirm_add,localConfirm_add,importedCase_add,noInfect_add from history ORDER BY ds desc LIMIT 1'
    cur.execute(dt1)
    data1 = cur.fetchall()[0]
    # 现有
    dt2 = 'SELECT nowConfirm,localConfirmH5,nowSevere,noInfect from history ORDER BY ds desc LIMIT 1'
    cur.execute(dt2)
    data2 = cur.fetchall()[0]
    # 累计
    dt3 = 'SELECT confirm,importedCase,heal,dead from history ORDER BY ds desc LIMIT 1'
    cur.execute(dt3)
    data3 = cur.fetchall()[0]

    # 各个城市数据
    city_dt = 'SELECT city,province,confirm_add,nowConfirm from details ORDER BY update_time desc LIMIT 60'
    cur.execute(city_dt)
    city_data = cur.fetchall()

    # 省数据
    province_dt = 'SELECT * FROM ' \
          '(select province,sum(confirm_add),sum(confirm),sum(heal),sum(dead) as de from details  ' \
          'where update_time=(select update_time from details ' \
          'order by update_time desc limit 1) ' \
          'group by province) as a ' \
          'ORDER BY de DESC'
    cur.execute(province_dt)
    province_data = cur.fetchall()

    # 实时播报
    hots = 'SELECT data,content,href FROM hotsearch ORDER BY data desc LIMIT 20'
    cur.execute(hots)
    hot = cur.fetchall()
    # conn.close()
    return render_template('index.html',
                           data1=data1,
                           data2=data2,
                           data3=data3,
                           city_data=city_data,
                           hot=hot,
                           province_data=province_data)


@app.route("/confirmmap")
def confirm():
    sql = 'SELECT province,confirm FROM ' \
          '(select province ,sum(nowConfirm) as confirm from details  ' \
          'where update_time=(select update_time from details ' \
          'order by update_time desc limit 1) ' \
          'group by province) as a ' \
          'ORDER BY confirm DESC'
    detdata = query(sql)
    res = []

    for tup in detdata:
        res.append({"name": tup[0], "value": int(tup[1])})
    return jsonify({"data": res})


@app.route("/caddmap")
def conadd():
    sql = 'SELECT province,confirm FROM ' \
          '(select province ,sum(confirm_add) as confirm from details  ' \
          'where update_time=(select update_time from details ' \
          'order by update_time desc limit 1) ' \
          'group by province) as a ' \
          'ORDER BY confirm DESC'
    detdata = query(sql)
    res = []

    for tup in detdata:
        res.append({"name": tup[0], "value": int(tup[1])})
    return jsonify({"data": res})


@app.route("/localdata")
def data():
    sql = 'SELECT ds,localConfirm_add from history WHERE TO_DAYS( NOW( ) ) - TO_DAYS( ds )<=10'
    hisData = query(sql)
    date, localConfirm_add = [], []
    for a, q in hisData:
        date.append(a.strftime("%m.%d"))
        localConfirm_add.append(q)
    return jsonify({"date": date, "localConfirm_add": localConfirm_add})


@app.route("/impdata")
def impdata():
    sql = 'SELECT ds,importedCase_add from history WHERE TO_DAYS( NOW( ) ) - TO_DAYS( ds )<=10'
    hisData = query(sql)
    date, importedCase_add = [], []
    for a, e in hisData:
        date.append(a.strftime("%m.%d"))
        importedCase_add.append(e)
    return jsonify({"date": date, "importedCase_add": importedCase_add})


@app.route("/newdata")
def newdata():
    sql = 'SELECT ds,importedCase_add,confirm from history WHERE TO_DAYS( NOW( ) ) - TO_DAYS( ds )<=10'
    hisData = query(sql)
    date, importedCase_add, confirm = [], [], []
    for a, e, f in hisData:
        date.append(a.strftime("%m.%d"))

        importedCase_add.append(e)
        confirm.append(f)
    return jsonify({
        "date": date,
        "importedCase_add": importedCase_add,
        "confirm": confirm
    })


@app.route("/nodata")
def nodata():
    sql = 'SELECT ds,nowConfirm,confirm,noInfect from history WHERE TO_DAYS( NOW( ) ) - TO_DAYS( ds )<=10'
    hisData = query(sql)
    date, nowConfirm, confirm, noInfect = [], [], [], []
    for a, c, f, h in hisData:
        date.append(a.strftime("%m.%d"))

        nowConfirm.append(c)
        confirm.append(f)
        noInfect.append(h)
    return jsonify({
        "date": date,
        "nowConfirm": nowConfirm,
        "confirm": confirm,
        "noInfect": noInfect
    })


@app.route("/healdata")
def healdata():
    sql = sql = 'SELECT ds,heal,dead from history WHERE TO_DAYS( NOW( ) ) - TO_DAYS( ds )<=10'
    healData = query(sql)
    date, heal, dead = [], [], []
    for a, l, n in healData:
        date.append(a.strftime("%m.%d"))
        heal.append(l)
        dead.append(n)

    return jsonify({"date": date, "heal": heal, "dead": dead})


# 各省主页
@app.route("/<name>")
def province(name):
    provinceName = [
        '台湾', '上海', '香港', '北京', '四川', '河南', '天津', '福建', '吉林', '广东', '云南', '浙江',
        '青海', '山东', '辽宁', '广西', '江苏', '河北', '湖南', '贵州', '黑龙江', '江西', '山西',
        '内蒙古', '陕西', '甘肃', '湖北', '海南', '澳门', '新疆', '安徽', '宁夏', '西藏', '重庆'
    ]
    data_sql1 = 'SELECT * FROM (select sum(nowConfirm),sum(confirm_add),sum(confirm),sum(heal),sum(dead) as de from details  where province=\"'
    data_sql2 = '\" and update_time=(select update_time from details order by update_time desc limit 1) group by update_time) as a ORDER BY de DESC'
    data_sql3 = 'SELECT * FROM (select city,confirm_add,confirm,heal,dead as de from details where update_time=(select update_time from details order by update_time desc limit 1) and province=\"'
    data_sql4 = '\" group by city) as a ORDER BY de DESC'
    for i in provinceName:
        if (name == i):
            sql = data_sql1 + i + data_sql2

            cur.execute(sql)
            data1 = cur.fetchall()[0]
            sql1 = data_sql3 + i + data_sql4
            cur.execute(sql1)4
            data2 = cur.fetchall()
            return render_template('common.html', data1=data1, data2=data2)


# 省数据接口
@app.route("/provincedata/<name>")
def provincedate(name):
    date_sql = "SELECT * FROM (select update_time as time from details where TO_DAYS( NOW( ) ) - TO_DAYS( update_time )<=10 group by update_time) as a order by time asc limit 10"
    updateTime = query(date_sql)
    date, c = [], []
    for a in updateTime:
        # print("----------------------------------------------------------------")
        # print(a)
        date.append(a[0].strftime("%m.%d"))
    # print(date)
    provinceName = [
        '台湾', '上海', '香港', '北京', '四川', '河南', '天津', '福建', '吉林', '广东', '云南', '浙江',
        '青海', '山东', '辽宁', '广西', '江苏', '河北', '湖南', '贵州', '黑龙江', '江西', '山西',
        '内蒙古', '陕西', '甘肃', '湖北', '海南', '澳门', '新疆', '安徽', '宁夏', '西藏', '重庆'
    ]
    data_sql1 = 'SELECT * FROM (select sum(confirm_add),sum(confirm),sum(heal),sum(dead) as de from details  where province=\"'
    data_sql2 = '\" and TO_DAYS( NOW( ) ) - TO_DAYS( update_time )<=10 group by update_time) as a ORDER BY de DESC limit 10'
    for a in provinceName:
        # 对比发送数据地址与查询省名称匹配，如果一致，则会将数据发送到该地址，动态route应用
        if (name == a):
            # print(name)
            data_sql = data_sql1 + a + data_sql2
            provincedata = query(data_sql)
            confiirm_add, confirm, heal, dead = [], [], [], []
            for b, c, d, e in provincedata:
                confiirm_add.append(b)
                confirm.append(c)
                heal.append(d)
                dead.append(e)
            return jsonify({
                "date": date,
                "confirm_add": confiirm_add,
                "confirm": confirm,
                "heal": heal,
                "dead": dead
            })


if __name__ == '__main__':
    app.run(debug=True)
