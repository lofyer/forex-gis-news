#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

from __future__ import print_function, unicode_literals
import MySQLdb
import jieba
import sys

jieba.enable_parallel(4)
jieba.load_userdict("dict.txt.big")

def cuttest(test_sent):
    result = jieba.cut(test_sent, cut_all=True)
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
print(data)

#
# Processing data here
#

cursor.execute("select id,title,content,url,date_format(str_to_date(date, '%d-%M-%Y'), '%Y%m%d') as date_new from posts where id>1300000;")
data = cursor.fetchall()
for d in data:
    #print(d[1])
    cuttest(d[1])

db.close()
