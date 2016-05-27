# coding:utf-8
import MySQLdb
import json

finalRandom = 1
#receive json data from web
data = {
    'id' : '3115034018',
    'captain' : '董怡卓',
    'dorm' : '217' ,
	'random' : 1
}
tmp = json.dumps(data)
chooseInfo = json.loads(tmp)
if chooseInfo['random']!=finalRandom:
	print "不许用脚本"

#connect to mysql
conn= MySQLdb.connect(
        host='localhost',
        port = 3306,
        user='root',
        passwd='123123',
        db ='choosedorm',
        )
cur = conn.cursor()

#jugde logical
groupitem = cur.execute("select * from GroupTable where captainID="+chooseInfo['id'])
if groupitem==0:
	print "无该组信息"

groupInfo = cur.fetchmany(groupitem)[0]

if chooseInfo['captain'] != groupInfo[1].decode('gbk'):
	print "队长信息有误"
if groupInfo[6]!=-1:
	print "此队已选过，不能再更改"

#choose logical
dormitem = cur.execute("select * from DormTable where dormID="+chooseInfo['dorm'])
if dormitem==0:
	print "无此宿舍"

dormInfo = cur.fetchmany(dormitem)[0]

if groupInfo[2] > dormInfo[1]:
	print "此宿舍床位不够"

#write dorm info
#4 member, write directly
if groupInfo[2]==4:
	s = "update DormTable SET remainBed=%s,bed1=%s,bed2=%s,bed3=%s,bed4=%s where dormID="+chooseInfo['dorm']
	cur.execute(s,(str(dormInfo[1]-groupInfo[2]),groupInfo[1],groupInfo[3],groupInfo[4],groupInfo[5]))
#less than 4 member, combine and write
else:
	newMemList = []
	newMemSum = 4-dormInfo[1]+groupInfo[2]
	for i in range(0,4-dormInfo[1]):
		newMemList.append(dormInfo[2+i])
	newMemList.append(groupInfo[1])
	for j in range(0,groupInfo[2]-1):
		newMemList.append(groupInfo[3+j])
	for k in range(0,4-newMemSum):
		newMemList.append("")
	s = "update DormTable SET remainBed=%s,bed1=%s,bed2=%s,bed3=%s,bed4=%s where dormID="+chooseInfo['dorm']
	#cur.execute("SET NAMES utf8;")
	cur.execute(s,(str(dormInfo[1]-groupInfo[2]),newMemList[0],newMemList[1],newMemList[2],newMemList[3]))

cur.execute("update GroupTable SET dormID="+str(dormInfo[0])+" where captainID="+chooseInfo['id'])

#search dorm info
dormitem = cur.execute("select * from DormTable where dormID="+chooseInfo['dorm'])
dormInfo = cur.fetchmany(dormitem)[0]
print "选择成功，该宿舍信息为："
print dormInfo[0],dormInfo[1],dormInfo[2].decode('gbk'),dormInfo[3].decode('gbk'),dormInfo[4].decode('gbk'),dormInfo[5].decode('gbk')

cur.close()
conn.commit()
conn.close()

