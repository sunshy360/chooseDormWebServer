# coding:utf-8
from django.http import HttpResponse
from django.shortcuts import render_to_response
import MySQLdb
import json
import traceback

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
			user='choosedorm',
			passwd='choosedorm',
			db ='choosedorm',
			charset='utf8',
			)
	cur = conn.cursor()

	if request.method == 'POST':
                print request.body
		chooseInfo = json.loads(request.body)
		if chooseInfo['random']!=finalRandom:
			print "不许用脚本"
                        return HttpResponse("400")
		return POST(chooseInfo)
	elif request.method == 'GET':
		return GET()

def POST(chooseInfo):
        try:
	        #jugde logical
	        groupitem = cur.execute("select * from GroupTable where captainID="+chooseInfo['id']+"")
	        if groupitem==0:
	        	commitandclose()
                        # Error Code: 401: 无该组信息
	        	return HttpResponse("401")

	        groupInfos = cur.fetchmany(groupitem)

                print groupInfos
                # Error Code: 501: 并发错误
                if len(groupInfos) != 1:
                        return HttpResponse("501")
	        groupInfo = groupInfos[0]

	        #if chooseInfo['captain'] != groupInfo[1].decode('utf8'):
	        if chooseInfo['captain'] != groupInfo[1]:
	        	commitandclose()
                        # Error Code 402: 队长信息有误
	        	return HttpResponse("402")
	        if groupInfo[6]!=-1:
	        	commitandclose()
                        # Error Code: 403:此队已经选过 
	        	return HttpResponse("403")

	        #choose logical
	        dormitem = cur.execute("select * from DormTable where dormID="+str(chooseInfo['dorm']))
	        if dormitem==0:
	        	commitandclose()
                        # Error Code: 404:无此宿舍
	        	return HttpResponse("404")

	        dormInfo = cur.fetchmany(dormitem)[0]

	        if groupInfo[2] > dormInfo[1]:
	        	commitandclose()
                        # Error Code: 405:此宿舍床位不够
	        	return HttpResponse("405")

	        #write dorm info
	        #4 member, write directly
	        if groupInfo[2]==4:
	        	s = "update DormTable SET remainBed=%s,bed1=%s,bed2=%s,bed3=%s,bed4=%s where dormID="+str(chooseInfo['dorm'])
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
	        	s = "update DormTable SET remainBed=%s,bed1=%s,bed2=%s,bed3=%s,bed4=%s where dormID="+str(chooseInfo['dorm'])
	        	#cur.execute("SET NAMES utf8;")
	        	cur.execute(s,(str(dormInfo[1]-groupInfo[2]),newMemList[0],newMemList[1],newMemList[2],newMemList[3]))

	        cur.execute("update GroupTable SET dormID="+str(dormInfo[0])+" where captainID="+chooseInfo['id'])

	        #search dorm info
	        dormitem = cur.execute("select * from DormTable where dormID="+str(chooseInfo['dorm']))
	        dormInfo = cur.fetchmany(dormitem)[0]

	        commitandclose()
                print "OK!OK!OK!OK!OK!OK!"
	        return HttpResponse("200")
        except Exception,e:
                traceback.print_exc()
                return HttpResponse("501")

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
	jsonList = json.dumps(jsonList)
	commitandclose()
	return HttpResponse(jsonList)

def commitandclose():
	cur.close()
	conn.commit()
	conn.close()
