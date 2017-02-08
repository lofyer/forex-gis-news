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
sql_cmd = 'select id,title,content,url,date,content_hash from posts where id > 50000 and id < 55000'
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
    title_word_list = jieba.cut((d[1]), cut_all=False)
    content_word_list = jieba.cut((d[2]), cut_all=False)
    placed = False
    # from title
    for t in title_word_list:
        for c in countries_all:
            if t == c[0]:
                nplaced += 1
                placed = True
                print(t)
    # from content
    if placed == False:
        for t in content_word_list:
            for c in countries_all:
                if t == c[0]:
                    nplaced += 1
                    placed = True
                    print(t)

    #sql = "update rss_rating (content_hash) values %d where content_hash=%s" % (d[5], d[5])
    #cursor.execute(sql)

print(nplaced)
print(nnews)
print('Percent of placed: %f' % (nplaced/nnews))

#db.commit()
db.close()
