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
# country list
sql_cmd = "select country from city_map group by country;"
cursor.execute(sql_cmd)
countries_all = cursor.fetchall()

# city list
sql_cmd = "select city from city_map group by city;"
cursor.execute(sql_cmd)
cities_all = cursor.fetchall()
print(cities_all)

#
# Process news from right here
#

# Get news
sql_cmd = 'select id,title,content,url,date,content_hash from posts where id > 100000 and id < 105000;'
print(sql_cmd)
cursor.execute(sql_cmd)
data = cursor.fetchall()

#
# STEP 1: which country
#
nplaced = 0.0
nnews = len(data)
for d in data:
    if d == "":
        continue
    print("ID: %d" % d[0])
    #print("Title: %s" % d[1])
    title_word_list = list(jieba.cut((d[1]), cut_all=False))
    content_word_list = list(jieba.cut((d[2]), cut_all=False))
    placed = False

    # for title in country list
    for t in title_word_list:
        for c in countries_all:
            if t == c[0]:
                nplaced += 1
                placed = True
                print(t)

    # for title in city list
    if placed == False:
        for t in title_word_list:
            for c in cities_all:
                if t == c[0]:
                    nplaced += 1
                    cmd = 'select country from city_map where city=%s;' % t
                    cursor.execute(sql_cmd)
                    selected_city = cursor.fetchall()
                    placed = True
                    print("+++++++++++++++++++++++++++++")
                    print(selected_city[0])

    #sql = "update rss_rating (content_hash) values %d where content_hash=%s" % (d[5], d[5])
    #cursor.execute(sql)

print(nplaced)
print(nnews)
print('Percent of placed: %f' % (nplaced/nnews))

#db.commit()
db.close()
