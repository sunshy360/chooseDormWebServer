# coding:utf-8
import MySQLdb

conn= MySQLdb.connect(
        host='localhost',
        port = 3306,
        user='root',
        passwd='123123',
        db ='choosedorm',
        )
cur = conn.cursor()

for i in range(1,4):
	for j in range(1,10):
		cur.execute("insert into DormTable (dormID) values("+str(i)+"0"+str(j)+")")
	for j in range(10,21):
		cur.execute("insert into DormTable (dormID) values("+str(i)+str(j)+")")

cur.close()
conn.commit()
conn.close()

