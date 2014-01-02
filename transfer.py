# -*- coding: utf-8 -*-
import os
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import MySQLdb

conn1 = MySQLdb.connect(host="58.205.208.72",user="root",passwd="root",charset="utf8")
conn1.select_db('experts')
cursor1 = conn1.cursor()
cursor1.execute("SET NAMES utf8")
cursor1.execute("SET NAMES utf8")
cursor1.execute("SET CHARACTER_SET_CLIENT=utf8")
cursor1.execute("SET CHARACTER_SET_RESULTS=utf8")
conn1.commit()

conn2 = MySQLdb.connect(host="166.111.81.223",user="root",passwd="root",charset="utf8")
conn2.select_db('experts')
cursor2 = conn2.cursor()
cursor2.execute("SET NAMES utf8")
cursor2.execute("SET NAMES utf8")
cursor2.execute("SET CHARACTER_SET_CLIENT=utf8")
cursor2.execute("SET CHARACTER_SET_RESULTS=utf8")
conn2.commit()

count = 0
while(True):
    sql = "select Expert_ID,Expert_name,Expert_keywords from GeniusExpert limit "+(count*1000).__str__()+","+(count*1000+1000).__str__()+";"
    print sql
    cursor1.execute(sql)
    row_count = 0
    for row in cursor1.fetchall():
        row_count += 1
        sql = "insert into web_expert expertID,expertName,keywords values({0},\"{1}\",\"{2}\"".format(row[0],row[1],row[2])
        cursor2.execute(sql)
    cursor2.commit()
    if row_count<1001:
        break
    count += 1
print 'ok'
count = 0
'''
while(True):
    sql = "select expert_ID,title,authorlist,pub_date from CnkiPaper limit "+(count*1000).__str__()+","+(count*1000+1000).__str__()+";"
    print sql
    cursor1.execute(sql)
    row_count = 0
    for row in cursor1.fetchall():
        row_count += 1
        print row
    if row_count<1001:
        break
    count += 1
'''
