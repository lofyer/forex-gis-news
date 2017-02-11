#!/usr/local/bin/python
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
f = open('./rss_source.txt', 'r')
data = f.readlines()

for link in data:
    sql_cmd = 'insert into rss_source (link) values ("%s");' % (link.strip())
    try:
        cursor.execute(sql_cmd)
    except Exception as e:
        print e

db.commit()
db.close()
