# coding:utf-8
import csv
import MySQLdb

csvfile = file('group.csv', 'rb')
csvfile.readline()
reader = csv.reader(csvfile)

conn= MySQLdb.connect(
        host='localhost',
        port = 3306,
        user='root',
        passwd='123123',
        db ='choosedorm',
        )
cur = conn.cursor()

for line in reader:
	#print line[2],line[1].decode("gbk").encode("utf-8"),line[0],line[3].decode("gbk").encode("utf-8"),line[4].decode("gbk").encode("utf-8"),line[5].decode("gbk").encode("utf-8")
	s = "insert into GroupTable values(%s,%s,%s,%s,%s,%s,%s)"
	cur.execute(s,(line[2],line[1],line[0],line[3],line[4],line[5],'-1'))

csvfile.close()

cur.close()
conn.commit()
conn.close()

'''
create table GroupTable(
    -> captainID int(10) not null primary key,
    -> captainName varchar(20) not null,
    -> number int(1) not null,
    -> member1 varchar(20) not null,
    -> member2 varchar(20),
    -> member3 varchar(20),
    -> member4 varchar(20),
    -> dormID int(4) default -1);
'''
