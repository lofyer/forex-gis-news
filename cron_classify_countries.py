#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

#
# This script will update the rss_rating:rss_rating:(id, content_hash, country)
#

from datetime import date
from multiprocessing.dummy import Pool
import jieba
import sys
import pymysql
import pymysql.cursors

jieba.enable_parallel(4)
jieba.load_userdict("./jieba/extra_dict/dict.txt.big")

db = pymysql.connect(
    host = "localhost",
    port = 3306,
    user = "root",
    passwd = "123456",
    db = "rss",
    charset = 'utf8'
    )
    #cursorclass = pymysql.cursors.SSCursor) ### No longer needed in pymysql
db.autocommit(1)
cursor = db.cursor()

### country list
sql_cmd = "select country from city_map group by country;"
cursor.execute(sql_cmd)
countries_all = [ x[0] for x in cursor.fetchall() ]

### city and country list, avoid frequent querying from db
sql_cmd = "select city,country from city_map group by city;"
cursor.execute(sql_cmd)
cities_countries_all = cursor.fetchall()
cities_all = [ x[0] for x in cities_countries_all ]
countries_of_cities_all = [ x[1] for x in cities_countries_all ]

### Get news
sql_cmd = 'select id,title,content,url,date,content_hash from posts where date_format(str_to_date(date, '%d-%M-%Y'), '%Y%m%d')=curdate()+0;'

print(sql_cmd)
cursor.execute(sql_cmd)
news_all = list(cursor.fetchall())


### STEP 1: which country

nplaced = 0.0
nnews = len(news_all)

def search_place(news):
    global nplaced
    global cursor
    print("ID: %d" % news[0])
    title_word_list = list(jieba.cut((news[1]), cut_all=False))
    #content_word_list = list(jieba.cut((news[2]), cut_all=False))

    for t in title_word_list:
        if t in countries_all:
            nplaced += 1
            #print(t)
            sql_cmd = 'insert into rss_rating (id, content_hash, country) values ("%s", "%s", "%s") ON DUPLICATE KEY UPDATE country="%s";' % (news[0], news[5], t, t)
            cursor.execute(sql_cmd)
            ### Use return rather than break
            return 0
        elif t in cities_all:
            nplaced += 1
            #print(countries_of_cities_all[cities_all.index(t)])
            t_country = countries_of_cities_all[cities_all.index(t)]
            sql_cmd = 'insert into rss_rating (id, content_hash, country) values ("%s", "%s", "%s") ON DUPLICATE KEY UPDATE country="%s";' % (news[0], news[5], t, t)
            cursor.execute(sql_cmd)
            return 0
    return 1

pool1 = Pool()
pool1.map(search_place, news_all)
pool1.close()
pool1.join()

print(nplaced)
print(nnews)
print('Percent of placed: %f' % (nplaced/nnews))

#db.commit() ### Use autocommit()
cursor.close()
db.close()
