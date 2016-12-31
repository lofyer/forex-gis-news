#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
import MySQLdb
import json

db = MySQLdb.connect("localhost",
    "root",
    "123456",
    "rss" )
cursor = db.cursor()

f1 = open('./countriesToCities.json', 'r')
f2 = open('./country-list.json', 'r')
json_data1 = json.load(fp = f1)
json_data2 = json.load(fp = f2)

for country in json_data1.iterkeys():
    for city in json_data1[country]:
        if city == "":
            continue
        sql_cmd = 'insert into city_map (city, country) values ("%s", "%s");' % (city, country)
        # Following for is to search coninent and iso name
        # a: country_iso, b: country, c: continent
        for c in json_data2.iterkeys():
            for a,b in json_data2[c].iteritems():
                if b == country:
                    sql_cmd = 'insert into city_map (city, country, country_iso, continent) values ("%s", "%s", "%s", "%s");' % (city, country, a, c)

        try:
            cursor.execute(sql_cmd)
            print
        except Exception as e:
            print e

db.commit()
db.close()
