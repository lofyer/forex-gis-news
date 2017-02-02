#!/usr/local/bin/python
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
        print(word, "/", end=' ') 
    print("")

db = MySQLdb.connect("localhost",
    "root",
    "123456",
    "rss" )
cursor = db.cursor()
cursor.execute("show columns from posts")
data = cursor.fetchall()

# show columns
print(data)

#
# Process data here
#

sql_cmd = 'select id,title,content,url,date from posts where id < 20000'
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
    cuttest(d[1])
    #sql = "update rss_rating (id) values %d where id=%d" % (d[0], d[0])
    #cursor.execute(sql)

#db.commit()
db.close()