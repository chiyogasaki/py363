#!/usr/bin/env python
# -*- coding: utf-8 -*-
    
from xml.etree.ElementTree import parse
from urllib.parse import quote  
import urllib.request, urllib.error
import csv
from math import sin, cos, acos, radians
import urllib.request, json
import urllib.parse
import datetime
import time
import pandas as pd
import numpy as np
from ast import literal_eval
import os


#住所から経度・緯度を求める関数
def adr2geo(adr):
    api = "http://www.geocoding.jp/api/?v=1.1&q=%s" % (quote(adr.encode('utf-8')))
    xml = parse(urllib.request.urlopen(api)).getroot()

    lat = xml.find('coordinate/lat').text
    lng = xml.find('coordinate/lng').text
    return (float(lat), float(lng))

#２地点の直線距離を求める関数
earth_rad = 6378.137

def latlng_to_xyz(lat, lng):
    rlat, rlng = radians(lat), radians(lng)
    coslat = cos(rlat)
    return coslat*cos(rlng), coslat*sin(rlng), sin(rlat)

def dist_on_sphere(pos0, pos1, radious=earth_rad):
    xyz0, xyz1 = latlng_to_xyz(*pos0), latlng_to_xyz(*pos1)
    return acos(sum(x * y for x, y in zip(xyz0, xyz1)))*radious


#元データの読み込み
with open("test.csv", 'r') as f:
    reader = csv.reader(f)
    header = next(reader) #ヘッダーの読み飛ばし
    lst = list(csv.reader(f))


points = []
if os.path.exists("./data.csv"):
    print("data.csvがすでにあります.更新する際は手動でdata.csvを削除してください。")
    

else: #data.csvの作成
    for s in lst:
        address = s[3]
        lnglat = adr2geo(address)
        s.append(lnglat)
        points.append(s)
        time.sleep(10)

    print(points)




    startpoint_name = "福岡県遠賀郡水巻町下ニ西3-6-15"
    startpoint = adr2geo(startpoint_name)

    alldata = []

    for b in points:
        point = b[4]
        dia = dist_on_sphere(startpoint,point)
        b.append(dia)
        alldata.append(b)

    #print(type(point))

    #print(alldata)

    with open("data.csv",'w') as f:
        writer = csv.writer(f)
        writer.writerow(["起点",startpoint_name])
        writer.writerow(["組","名前","のる・のらない","住所","経度・緯度","起点からの距離"])
        for e in alldata:
            writer.writerow(e)

#data.csvの読み込み
df = pd.read_csv('data.csv', header=1)
df_sort = df.sort_values("起点からの距離")
bus_stop = df_sort.values.tolist()
#経度・緯度がstrになってしまっているのでtupleに変換
for x in bus_stop:
    x[4] = literal_eval(x[4])

#幼稚園からの直線距離でAバスとBバスに分ける
abus = []
bbus = []
for x in bus_stop:
    if 0.7 > x[5]:
        abus.append(x)
    else:
        bbus.append(x)



#Aバスのバス停を並べる
print("★===================================================")
print("Aバスのバス停候補:",abus)
print("=========================")
abus_stop = abus
abus_stop = np.array(abus_stop)


abus_stop2 = [[abus[0]]] #abus_stop2に１番目のバス停を含める（幼稚園から最短の場所）
while 1 < len(abus_stop):
    #print(len(abus_stop))
    abus_stop = np.delete(abus_stop, 5, axis = 1)
    abus_stop = np.insert(abus_stop, 5, x[5], axis=1)
    abus_stop = np.delete(abus_stop, 0, 0)

    for x in abus_stop:
        start = abus_stop[0][4]
        stop = x[4]
        x[5] = dist_on_sphere(start,stop)
        #print(x)
        #bus_stop3.append(x)
    abus_stop = abus_stop[abus_stop[:,5].argsort(), :]
    #print(bus_stop2)
    abus_stop2.append(abus_stop.tolist())
else:
    abus_route = []
    for x in abus_stop2:
        #print(x)
        abus_route.append(x[0])
    abus_route = np.array(abus_route)
#    print("Aバスのバス停並び：",abus_route)
#    print("=====================")
    print("=========================")
    print("Aバスの並び===============")
    print("=========================")
    print("===住所のみ表示"+"0"+"番:","幼稚園")
    a = 1
    for x in abus_route:
        print("↓")
        print("===住所のみ表示"+str(a)+"番:",x[3])
        a += 1


#Bバスのバス停を並べる
print("★===================================================")
print("Bバスのバス停候補:",bbus)
bbus_stop = bbus
bbus_stop = np.array(bbus_stop)


bbus_stop2 = [[bbus[0]]] #abus_stop2に１番目のバス停を含める（幼稚園から最短の場所）
while 1 < len(bbus_stop):
    #print(len(abus_stop))
    bbus_stop = np.delete(bbus_stop, 5, axis = 1)
    bbus_stop = np.insert(bbus_stop, 5, x[5], axis=1)
    bbus_stop = np.delete(bbus_stop, 0, 0)

    for x in bbus_stop:
        start = bbus_stop[0][4]
        stop = x[4]
        x[5] = dist_on_sphere(start,stop)
        #print(x)
        #bus_stop3.append(x)
    bbus_stop = bbus_stop[bbus_stop[:,5].argsort(), :]
    #print(bus_stop2)
    bbus_stop2.append(bbus_stop.tolist())
else:
    bbus_route = []
    for x in bbus_stop2:
        #print(x)
        bbus_route.append(x[0])
    bbus_route = np.array(bbus_route)
#    print("Aバスのバス停並び：",abus_route)
#    print("=====================")
    print("=========================")
    print("Bバスの並び===============")
    print("=========================")
    print("===住所のみ表示"+"0"+"番:","幼稚園")
    a = 1
    for x in bbus_route:
        print("↓")
        print("===住所のみ表示"+str(a)+"番:",x[3])
        a += 1
