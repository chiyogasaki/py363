#!/usr/bin/env python
# -*- coding: utf-8 -*-
	
from xml.etree.ElementTree import parse
from urllib.parse import quote  
import urllib.request, urllib.error
import csv

data = []
f = open("test.csv", "r")
reader = csv.reader(f)
header = next(reader)

for row in reader:
    data.append(row)





def adr2geo(adr):
    api = "http://www.geocoding.jp/api/?v=1.1&q=%s" % (quote(adr.encode('utf-8')))
    xml = parse(urllib.request.urlopen(api)).getroot()

    lat = xml.find('coordinate/lat').text
    lng = xml.find('coordinate/lng').text
    return (float(lat), float(lng))

print(adr2geo("北九州市若松区鴨生田4−９−２"))
	
def main():
    print(adr2geo('北九州市八幡西区千代ケ崎2-6-7-408'))

if __name__ == '__main__':
    main()





