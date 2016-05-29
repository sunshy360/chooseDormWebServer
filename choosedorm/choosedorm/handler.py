# coding:utf-8
from django.http import HttpResponse
from django.shortcuts import render_to_response
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

def choosedorm(request):

	#connect to mysql
	global conn
	global cur
	conn= MySQLdb.connect(
			host='localhost',
			port = 3306,
			user='root',
			passwd='123123',
			db ='choosedorm',
			)
	cur = conn.cursor()

	if request.method == 'POST':
		chooseInfo = json.loads(request.body)
		if chooseInfo['random']!=finalRandom:
			print "不许用脚本"
		return POST(chooseInfo)
	elif request.method == 'GET':
		return GET()

def POST(chooseInfo):

	#jugde logical
	groupitem = cur.execute("select * from GroupTable where captainID="+chooseInfo['id']+"FOR UPDATE")
	if groupitem==0:
		commitandclose()
		return HttpResponse("无该组信息".decode('utf8').encode("gbk"))

	groupInfo = cur.fetchmany(groupitem)[0]

	if chooseInfo['captain'] != groupInfo[1].decode('gbk'):
		commitandclose()
		return HttpResponse("队长信息有误".decode('utf8').encode("gbk"))
	if groupInfo[6]!=-1:
		commitandclose()
		return HttpResponse("此队已选过，不能再更改".decode('utf8').encode("gbk"))

	#choose logical
	dormitem = cur.execute("select * from DormTable where dormID="+chooseInfo['dorm']+"FOR UPDATE")
	if dormitem==0:
		commitandclose()
		return HttpResponse("无此宿舍".decode('utf8').encode("gbk"))

	dormInfo = cur.fetchmany(dormitem)[0]

	if groupInfo[2] > dormInfo[1]:
		commitandclose()
		return HttpResponse("此宿舍床位不够".decode('utf8').encode("gbk"))

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

	commitandclose()
	return HttpResponse("选择成功，该宿舍信息为：\n".decode('utf8').encode("gbk")+str(dormInfo[0])+" "+dormInfo[2]+" "+dormInfo[3]+" "+dormInfo[4]+" "+dormInfo[5])

def GET():

	dormitems = cur.execute("select * from DormTable")
	dormList = cur.fetchmany(dormitems)
	jsonList = []
	for item in dormList:
		jsonTmp = {
			'dormID' : item[0],
			'member1' : item[2],
			'member2' : item[3],
			'member3' : item[4],
			'member4' : item[5]
		}
		jsonList.append(jsonTmp)
	
	commitandclose()
	return HttpResponse(jsonList)

def commitandclose():
	cur.close()
	conn.commit()
	conn.close()
