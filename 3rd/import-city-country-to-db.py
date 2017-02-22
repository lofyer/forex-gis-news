#!/usr/local/bin/python2
# -*- coding: UTF-8 -*-
import MySQLdb
import json
import csv

db = MySQLdb.connect("localhost",
    "root",
    "123456",
    "rss" )
cursor = db.cursor()

# city in country: country, city
f1 = open('./countriesToCities.json', 'r')
json_data1 = json.load(fp = f1)
# country in continent
f2 = open('./country-list.json', 'r')
json_data2 = json.load(fp = f2)
# currency list
csv_data1 = []
csv_data2 = []
for i,o,p in csv.reader(open('./country-currency.csv')):
    csv_data1.append([i,o,p]) 
    csv_data2.append(i) 

for country in json_data1.iterkeys():
    for j in range(len(csv_data2)):
        if country in csv_data2[j]:
            cur = csv_data1[j][1]
            cur_iso = csv_data1[j][2]
            break
        else:
            cur = "NULL"
            cur_iso = "NULL"
        
    for city in json_data1[country]:
        if city == "":
            continue

        sql_cmd = 'insert into city_map (city, country, country_currency, country_currency_iso) values ("%s", "%s", "%s", "%s");' % (city, country, cur, cur_iso)
        # Following for is to search coninent and iso name
        # a: country_iso, b: country, c: continent
        for c in json_data2.iterkeys():
            for a,b in json_data2[c].iteritems():
                if b == country:
                    sql_cmd = 'insert into city_map (city, country, country_iso, continent, country_currency, country_currency_iso) values ("%s", "%s", "%s", "%s", "%s", "%s");' % (city, country, a, c, cur, cur_iso)

        try:
            cursor.execute(sql_cmd)
            #print sql_cmd
        except Exception as e:
            print e

db.commit()
db.close()
