#!/usr/bin/env python
# -*- coding: utf-8 -*-
	
from xml.etree.ElementTree import parse
from urllib.parse import quote  
import urllib.request, urllib.error
import csv
from math import sin, cos, acos, radians
from operator import itemgetter #ソートのキー指定

with open("test.csv", 'r') as f:
    reader = csv.reader(f)
    header = next(reader) #ヘッダーの読み飛ばし
    lst = list(csv.reader(f))




def adr2geo(adr):
    api = "http://www.geocoding.jp/api/?v=1.1&q=%s" % (quote(adr.encode('utf-8')))
    xml = parse(urllib.request.urlopen(api)).getroot()

    lat = xml.find('coordinate/lat').text
    lng = xml.find('coordinate/lng').text
    return (float(lat), float(lng))
    
points = []

for s in lst:
    address = s[3]
    lnglat = adr2geo(address)
    s.append(lnglat)
    points.append(s)


earth_rad = 6378.137

def latlng_to_xyz(lat, lng):
    rlat, rlng = radians(lat), radians(lng)
    coslat = cos(rlat)
    return coslat*cos(rlng), coslat*sin(rlng), sin(rlat)

def dist_on_sphere(pos0, pos1, radious=earth_rad):
    xyz0, xyz1 = latlng_to_xyz(*pos0), latlng_to_xyz(*pos1)
    return acos(sum(x * y for x, y in zip(xyz0, xyz1)))*radious


startpoint_name = "福岡県遠賀郡水巻町下ニ西3-6-15"
startpoint = adr2geo(startpoint_name)

alldata = []

for b in points:
    point = b[4]
    dia = dist_on_sphere(startpoint,point)
    b.append(dia)
    alldata.append(b)

with open("data.csv",'w') as f:
    writer = csv.writer(f)
    writer.writerow(["起点",startpoint_name])
    writer.writerow(["組","名前","のる・のらない","住所","経度・緯度","起点からの距離"])
    for e in alldata:
        writer.writerow(e)



alldata.sort(key=itemgetter(5))
#print(lst)

abus = []
bbus = []
for a in lst:
    dia = a[5]
    dia = float(dia)
    if dia < 1.0:
        abus.append(a)                
    else:
        bbus.append(a)

print("Aバス候補：")
print(abus)
print("Bバス候補：")
print(bbus)



