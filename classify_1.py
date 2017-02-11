#!/usr/local/bin/python2
# -*- coding: UTF-8 -*-

#
# This script will update the rss_rating:rss_rating:(id, content_hash, country)
#

from __future__ import print_function, unicode_literals
from datetime import date
from multiprocessing.dummy import Pool
import jieba
import sys
import MySQLdb

jieba.enable_parallel(4)
jieba.load_userdict("./jieba/extra_dict/dict.txt.big")

db = MySQLdb.connect("localhost",
    "root",
    "123456",
    "rss" )
cursor = db.cursor()

# country list
sql_cmd = "select country from city_map group by country;"
cursor.execute(sql_cmd)
countries_all = cursor.fetchall()

# city and country list, avoid frequent querying from db
sql_cmd = "select city,country from city_map group by city;"
cursor.execute(sql_cmd)
cities_all = [x[0] for x in cursor.fetchall()]

# Get news
sql_cmd = 'select id,title,content,url,date,content_hash from posts where id > 100000 and id < 105000;'
print(sql_cmd)
cursor.execute(sql_cmd)
news_all = list(cursor.fetchall())

#
# STEP 1: which country
#

nplaced = 0.0
nnews = len(news_all)

def search_place(news):
    global nplaced
    print("ID: %d" % news[0])
    title_word_list = list(jieba.cut((news[1]), cut_all=False))
    #content_word_list = list(jieba.cut((news[2]), cut_all=False))

    # for title in country list
    for t in title_word_list:
        if any(t in s[0] for s in countries_all):
            nplaced += 1
            print(t)
            #sql = "update rss_rating (content_hash) values %d where content_hash=%s" % (d[5], d[5])
            #cursor.execute(sql)
            # Use return rather than break
            return 0
        elif any(t in s[1] for s in cities_all):
            nplaced += 1
            selected_city = cursor.fetchall()
            print(selected_city[0][0])
            #sql = "update rss_rating (content_hash) values %d where content_hash=%s" % (d[5], d[5])
            #cursor.execute(sql)
            return 0

pool1 = Pool(4)
pool1.map(search_place, news_all)
pool1.close()
pool1.join()

print(nplaced)
print(nnews)
print('Percent of placed: %f' % (nplaced/nnews))
exit()

#db.commit()
db.close()
