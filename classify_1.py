#!/usr/local/bin/python2
# -*- coding: UTF-8 -*-

#
# This script will update the rss_rating:rss_rating:(id, content_hash, country)
#

from __future__ import print_function, unicode_literals
from datetime import date
import jieba
import sys
import MySQLdb

jieba.enable_parallel(4)
jieba.load_userdict("./jieba/extra_dict/dict.txt.big")

def cuttest(test_sent):
    result = jieba.cut(test_sent, cut_all=False)
    for word in result:
        print(word, end=' ') 
    print("")

db = MySQLdb.connect("localhost",
    "root",
    "123456",
    "rss" )
cursor = db.cursor()

# show columns
sql_cmd = "select country from city_map group by country;"
cursor.execute(sql_cmd)
countries_all = cursor.fetchall()

#
# Process news from right here
#

# Get news
sql_cmd = 'select id,title,content,url,date from posts where id < 200'
print(sql_cmd)
cursor.execute(sql_cmd)
data = cursor.fetchall()

#
# STEP 1: which country?
#
for d in data:
    if d == "":
        continue
    print(d[0])
    print(d[1])
    title = jieba.cut((d[1]), cut_all=False)
    for t in title:
        for c in countries_all:
            if t == c[0]:
                print(t)
                print("yes")
                print("yes")
                print("yes")
                print("yes")
                print("yes")
                print("yes")
                print("yes")
                print("yes")
    #sql = "update rss_rating (id) values %d where id=%d" % (d[0], d[0])
    #cursor.execute(sql)

#db.commit()
db.close()
