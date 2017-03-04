#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

from datetime import date
from multiprocessing.dummy import Pool
from geotext import GeoText
import sys
import pymysql
import pymysql.cursors

db = pymysql.connect(
    host = "localhost",
    port = 3306,
    user = "root",
    passwd = "123456",
    db = "rss"
    #charset = 'utf8'
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
sql_cmd = 'select id,title,content,url,date,content_hash from posts where id >= {0} and id < {1};'.format(sys.argv[1], sys.argv[2])
print(sql_cmd)
cursor.execute(sql_cmd)
news_all = list(cursor.fetchall())

nplaced = 0.0
nnews = len(news_all)

def search_place(news):
    global nplaced
    global cursor
    print("ID: {0}".format(news[0]))
    t = GeoText(news[1])
    if t.countries :
        nplaced += 1
        #print(t)
        for i in t.countries:
            print(i)
            sql_cmd = 'insert into rss_rating (id, content_hash, country) values ("{0}", "{1}", "{2}") ON DUPLICATE KEY UPDATE country="{3}";'.format(news[0], news[5], i, i)
            cursor.execute(sql_cmd)
        return 0
    if t.cities:
        nplaced += 1
        for i in t.cities:
            if i in cities_all:
            #print(countries_of_cities_all[cities_all.index(t)])
                t_country = countries_of_cities_all[cities_all.index(i)]
                sql_cmd = 'insert into rss_rating (id, content_hash, country) values ("{0}", "{1}", "{2}") ON DUPLICATE KEY UPDATE country="{3}";'.format(news[0], news[5], t_country, t_country)
                cursor.execute(sql_cmd)
                return 0
    return 1

# pymysql threadsafety is 1
# https://github.com/PyMySQL/PyMySQL/blob/master/pymysql/__init__.py#L37
# https://www.python.org/dev/peps/pep-0249/#threadsafety

#pool1 = Pool(2)
#pool1.map(search_place, news_all)
#pool1.close()
#pool1.join()

# single thread now

for i in news_all:
    search_place(i)

print(nplaced)
print(nnews)
print('Percent of placed: %f' % (nplaced/nnews))

#db.commit() ### Use autocommit()
cursor.close()
db.close()
