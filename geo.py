#!/usr/bin/env python
# -*- coding: utf-8 -*-
	
from xml.etree.ElementTree import parse
from urllib.parse import quote  
import urllib.request, urllib.error
import csv

with open("test.csv") as f:
    lst = list(csv.reader(f))


def adr2geo(adr):
    api = "http://www.geocoding.jp/api/?v=1.1&q=%s" % (quote(adr.encode('utf-8')))
    xml = parse(urllib.request.urlopen(api)).getroot()

    lat = xml.find('coordinate/lat').text
    lng = xml.find('coordinate/lng').text
    return (float(lat), float(lng))


lst2 = lst[1][3]

print(adr2geo(lst2))




