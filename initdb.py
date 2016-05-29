# coding:utf-8
import csv
import MySQLdb

#connect to mysql
conn= MySQLdb.connect(
        host='localhost',
        port = 3306,
        user='choosedorm',
        passwd='choosedorm',
        db ='choosedorm',
        )
cur = conn.cursor()

#clear grouptable
cur.execute("TRUNCATE TABLE GroupTable;")

#init grouptable
csvfile = file('group.csv', 'rb')
csvfile.readline()
reader = csv.reader(csvfile)

for line in reader:
	s = "insert into GroupTable values(%s,%s,%s,%s,%s,%s,%s)"
	cur.execute(s,(line[2],line[1],line[0],line[3],line[4],line[5],'-1'))

csvfile.close()

#clear dormtable
cur.execute("TRUNCATE TABLE DormTable;")
#init dormtable
for i in range(1,4):
	for j in range(1,10):
		cur.execute("insert into DormTable (dormID) values("+str(i)+"0"+str(j)+")")
	for j in range(10,21):
		cur.execute("insert into DormTable (dormID) values("+str(i)+str(j)+")")

cur.close()
conn.commit()
conn.close()

