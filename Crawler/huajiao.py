# -*- coding: utf-8 -*-

import sys
from urllib2 import urlopen
try:
	from bs4 import BeautifulSoup
except ImportError:
	from BeautifulSoup import BeautifulSoup # for bs 3
import re
import json
import pymysql
import time
import datetime

def getNowTime():
	return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

# filter out live ids from a url
def filterLiveIds(url):
	html = urlopen(url).read()
	#print html
	liveIds = set()
	bsObj = BeautifulSoup(html, "html.parser")
	#print bsObj.prettify()
	for link in bsObj.findAll("a", href=re.compile("^(/l/)")):
		#print link.prettify()
		if 'href' in link.attrs:
			newPage = link.attrs['href']
			#print newPage
			liveId = re.findall("[0-9]+", newPage)
			liveIds.add(liveId[0])
	return liveIds

# get live ids from campus girls page 999
def getLiveIdsFromCampusGirlsPage():
	liveIds = set()
	pageno = 0
	for pageno in range(9):
		liveIds |= filterLiveIds("http://www.huajiao.com/category/999?pageno=" + str(pageno+1))
		print liveIds
	return liveIds

# get live ids from goddess come page 2
def getLiveIdsFromGoddessComePage():
	liveIds = set()
	pageno = 0
	for pageno in range(10):
		liveIds |= filterLiveIds("http://www.huajiao.com/category/2?pageno=" + str(pageno+1))
		print liveIds
	return liveIds

# get live ids from any category
def getLiveIdsFromCategory(baseUrl="http://www.huajiao.com/category/", categoryNo=999, pageCount=8):
	liveIds = set()
	for pageno in range(int(pageCount)+1):
		liveIds |= filterLiveIds(baseUrl + categoryNo + "?pageno=" + str(pageno+1))
		print liveIds
	return liveIds

# get user id from live page
def getUserId_deprecated(liveId):
	html = urlopen("http://www.huajiao.com/" + "l/" + str(liveId))
	bsObj = BeautifulSoup(html, "html.parser")
	text = bsObj.title.get_text()
	print "Text: " + text
	res = re.findall("ID:[0-9]+", text)
	res = res[0].split(':')[1]
	print "UserId: " + res
	return res

def getUserId(liveId):
	html = urlopen("http://www.huajiao.com/" + "l/" + str(liveId))
	bsObj = BeautifulSoup(html, "html.parser")
	authorInfo = bsObj.findAll(id="author-info")
	authorId = authorInfo[0].findAll("p", class_="author-id")
	print authorId[0].text
	res = authorId[0].text.split(' ')[1]
	print "UserId: " + res
	return res


# get user data from user page
def getUserData(userId):
	html = urlopen("http://www.huajiao.com/user/" + str(userId))
	bsObj = BeautifulSoup(html, "html.parser")
	data = dict()
	try:
		userInfoObj = bsObj.find("div", {"id":"userInfo"})
		data['FAvatar'] = userInfoObj.find("div", {"class": "avatar"}).img.attrs['src']
		userId = userInfoObj.find("p", {"class":"user_id"}).get_text()
		data['FUserId'] = re.findall("[0-9]+", userId)[0]
		print("data['FUserId']: " + data['FUserId'])
		tmp = userInfoObj.h3.get_text('|', strip=True).split('|')
		#print("UserName: " + tmp[0].encode("utf8"))
		data['FUserName'] = tmp[0]
		data['FLevel'] = tmp[1]
		tmp = userInfoObj.find("ul", {"class":"clearfix"}).get_text('|', strip=True).split('|')
		data['FFollow'] = tmp[0]
		data['FFollowed'] = tmp[2]
		data['FSupported'] = tmp[4]
		data['FExperience'] = tmp[6]
		return data
	except AttributeError as e:
		print e
		print(str(userId) + ":html parse error in getUserData()")
		return 0

# get user history lives
def getUserLives(userId):
	try:
		url = "http://webh.huajiao.com/User/getUserFeeds?fmt=json&uid=" + str(userId)
		html = urlopen(url).read().decode('utf-8')
		jsonData = json.loads(html)
		if jsonData['errno'] != 0:
			print(str(userId) + "error occured in getUserFeeds for: " + jsonData['msg'])
			return 0
		if jsonData['data'] is None:
			print(str(userId) + "No live data occured in getUserFeeds for: " + jsonData['msg'])
			return 0
		return jsonData['data']['feeds']
	except Exception as e:
		print e
		return 0

def spiderUserDatas(baseUrl="http://www.huajiao.com/category/", categoryNo=999, pageCount=8):
	for liveId in getLiveIdsFromCategory(baseUrl, categoryNo, pageCount):
		userId = getUserId(liveId)
		userData = getUserData(userId)
		if userData:
			replaceUserData(userData)
	return 1

def spiderUserLives(nums):
	userIds = selectUserIds(nums)
	for userId in userIds:
		#print userId
		liveDatas = getUserLives(userId[0])
		if liveDatas == 0:
			continue
		for liveData in liveDatas:
			liveData['feed']['FUserId'] = userId[0]
			replaceUserLive(liveData['feed'])
	return 1

def getTimestamp():
	return (time.mktime(datetime.datetime.now().timetuple()))

def getMysqlConn():
	conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='777', db='huajiaogirls', charset='utf8mb4')
	return conn

def getUserCount():
	conn = getMysqlConn()
	cur = conn.cursor()
	cur.execute("USE huajiaogirls")
	cur.execute("set names utf8mb4")
	cur.execute("SELECT count(FUserId) from Tbl_Huajiao_User")
	ret = cur.fetchone()
	return ret[0]

def getLiveCount():
	conn = getMysqlConn()
	cur = conn.cursor()
	cur.execute("USE huajiaogirls")
	cur.execute("set names utf8mb4")
	cur.execute("SELECT count(FLiveId) from Tbl_Huajiao_Live")
	ret = cur.fetchone()
	return ret[0]

# Note all mysql fetchall() return an array of tuple, you need for e in arr e[0] e[1] e[2]... to access
def selectUserIds(num):
	conn = getMysqlConn()
	cur = conn.cursor()
	try:
		cur = conn.cursor()
		cur.execute("USE huajiaogirls")
		cur.execute("set names utf8mb4")
		cur.execute("SELECT FUserId FROM Tbl_Huajiao_User ORDER BY FScrapedTime DESC LIMIT " + str(num))
		ret = cur.fetchall()
		return ret
	except:
		print("selectUserIds except")
		return 0

# update user data
def replaceUserData(data):
	conn = getMysqlConn()
	cur = conn.cursor()
	try:
		cur.execute("USE huajiaogirls")
		cur.execute("set names utf8mb4")
		cur.execute("REPLACE INTO Tbl_Huajiao_User(FUserId,FUserName, FLevel, FFollow,FFollowed,FSupported,FExperience,FAvatar,FScrapedTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (int(data['FUserId']), data['FUserName'],int(data['FLevel']),int(data['FFollow']),int(data['FFollowed']), int(data['FSupported']), int(data['FExperience']), data['FAvatar'],getNowTime())
		)
		conn.commit()
	except pymysql.err.InternalError as e:
		print e
	except UnicodeEncodeError as e:
		print("replaceUserData except, userId=" + str(data['FUserId']))
		print e

# update user live data
def replaceUserLive(data):
	conn = getMysqlConn()
	cur = conn.cursor()
	try:
		#print(data)
		cur.execute("USE huajiaogirls")
		cur.execute("set names utf8mb4")
		cur.execute("REPLACE INTO Tbl_Huajiao_Live(FLiveId,FUserId,FWatches,FPraises,FReposts,FReplies,FPublishTimestamp,FTitle,FImage,FLocation,FScrapedTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s )", (int(data['relateid']),int(data['FUserId']), int(data['watches']),int(data['praises']),int(data['reposts']),int(data['replies']),int(data['publishtimestamp']),data['title'], data['image'], data['location'],getNowTime())
		)
		conn.commit()
	except pymysql.err.InternalError as e:
		print(e)

def main(argv):
	if len(argv) < 2:
		print("Usage: python huajiao.py [spiderUserDatas <categoryNo><pageCount> | spiderUserLives <UserIdNums>]")
		exit()
	if (argv[1] == 'spiderUserDatas'):
		baseUrl = "http://www.huajiao.com/category/"
		categoryNo = 2
		pageCount = 10
		if len(argv) == 4:
			categoryNo = argv[2]
			pageCount = argv[3]
		elif len(argv) == 3:
			print("Usage: python huajiao.py [spiderUserDatas <categoryNo><pageCount>]")
			exit()
		spiderUserDatas(baseUrl, categoryNo, pageCount)
	elif (argv[1] == 'spiderUserLives'):
		nums = 100
		if len(argv) == 3:
			nums = argv[2]
		elif len(argv) > 3:
			print("Usage: python huajiao.py [spiderUserLives <UserIdNums>]")
			exit()
		spiderUserLives(nums)
	elif (argv[1] == 'getUserCount'):
		print(getUserCount())
	elif (argv[1] == 'getLiveCount'):
		print(getLiveCount())
	else:
		print("Usage: python huajiao.py [spiderUserDatas|spiderUserLives|getUserCount|getLiveCount]")

if __name__ == '__main__':
	main(sys.argv)