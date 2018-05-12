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
import urllib2
import os
import pprint
import requests


reload(sys)
sys.setdefaultencoding('utf-8')

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
# def getLiveIdsFromCategory(baseUrl="http://www.huajiao.com/category/", categoryNo=999, pageCount=8):
# 	liveIds = set()
# 	for pageno in range(int(pageCount)+1):
# 		liveIds |= filterLiveIds(baseUrl + str(categoryNo) + "?pageno=" + str(pageno+1))
# 		#print liveIds
# 	return liveIds

fake = {u'author': {u'astro': u'\u9b54\u7faf\u5ea7',
              u'authorexp': 85858,
              u'authorlevel': 19,
              u'avatar': u'http://image.huajiao.com/d238d9aa9474b3ae326dff77f41b5e2b-100_100.jpg',
              u'exp': 1081380,
              u'followed': False,
              u'gender': u'F',
              u'is_author_task': 1,
              u'level': 24,
              u'medal': [{u'kind': u'tuhao', u'medal': u'2'}],
              u'nickname': u'\u2728\u751c\u97f3\u960130\u5f92\U0001f4a3\u5c0f3.5',
              u'signature': u'\u76f4\u64ad\u65f6\u95f4\u54681-5\u4e2d\u534812\u70b9-3.30\uff01\u5468\u672b\u65e98.00-12.30',
              u'uid': u'62079146',
              u'userCache': 1526091724,
              u'verified': True,
              u'verifiedinfo': {u'credentials': u'\u76f4\u64ad\u65f6\u95f4\u54681-5\u4e2d\u534812\u70b9-3.30\uff01\u5468\u672b\u65e98.00-12.30',
                                u'error': u'',
                                u'official': False,
                                u'realname': u'\u2728\u751c\u97f3\u960130\u5f92\U0001f4a3\u5c0f3.5',
                                u'status': 3,
                                u'type': 1}},
  u'creatime': u'2018-05-11 12:36:13',
  u'feed': {u'beans': 12151,
            u'cate_icon': u'http://img.s3.huajiao.com/Object.access/hj-img/cGhwSnl2b01Y',
            u'duration': 12381,
            u'favorited': False,
            u'feedCache': 0,
            u'feedid': 222069687,
            u'game': u'',
            u'height': 896,
            u'image': u'http://image.huajiao.com/d238d9aa9474b3ae326dff77f41b5e2b-320_320.jpg',
            u'is_game': u'N',
            u'is_link': u'N',
            u'is_outdoors': u'N',
            u'is_privacy': u'N',
            u'is_vr': u'N',
            u'labels': [u'\u6f14\u5458',
                        u'\u6027\u611f',
                        u'\u597d\u8eab\u6750',
                        u'\u6c14\u8d28',
                        u'\u4e2d\u56fd\u597d\u7f51\u6c11'],
            u'live_cate': u'\u8df3\u821e',
            u'origin_status': 1,
            u'praises': 1356,
            u'publishtime': u'2018-05-11 12:36:13',
            u'relateid': 225794113,
            u'replay_status': 1,
            u'replies': 0,
            u'reposts': 0,
            u'screenshot': u'',
            u'small_videos': 36,
            u'sn': u'_LC_ps4_non_6207914615260133721600572_OX',
            u'ss_height': 0,
            u'ss_width': 0,
            u'tags': [],
            u'title': u'\u563f',
            u'watches': 4347,
            u'width': 504},
  u'relay': {u'channel': u'live_huajiao_v2',
             u'usign': u'70ef6e3efdf0a318bfd5e64598f153cb'},
  u'type': 2}

# <ul class="clearfix">
# <li class="item" data-bk="category-1000"><a href="/category/1000" class="" target="_blank">热门</a></li>
# <li class="item" data-bk="category-812"><a href="/category/812" class="" target="_blank">吃鸡</a></li>
# <li class="item" data-bk="category-2"><a href="/category/2" class="" target="_blank">女神</a></li>
# <li class="item" data-bk="category-5"><a href="/category/5" class="" target="_blank">男神</a></li>
# <li class="item" data-bk="category-999"><a href="/category/999" class="" target="_blank">校园</a></li>
# <li class="item" data-bk="category-800"><a href="/category/800" class="" target="_blank">颜值</a></li>
# <li class="item" data-bk="category-806"><a href="/category/806" class="" target="_blank">脱口秀</a></li>
# <li class="item" data-bk="category-802"><a href="/category/802" class="" target="_blank">弹唱</a></li>
# <li class="item" data-bk="category-803"><a href="/category/803" class="" target="_blank">玩乐</a></li>
# <li class="item" data-bk="category-801"><a href="/category/801" class="" target="_blank">跳舞</a></li>
# <li class="item" data-bk="category-805"><a href="/category/805" class="" target="_blank">游戏</a></li>
# <li class="item" data-bk="category-811"><a href="/category/811" class="" target="_blank">娱乐明星</a></li>
# <li class="item" data-bk="category-810"><a href="/category/810" class="" target="_blank">城市之声</a></li>
# </ul>

category = {
	1000: "热门",
	812: "吃鸡",
	2: "女神",
	5: "男神",
	999: "校园",
	800: "颜值",
	806: "脱口秀",
	802: "弹唱",
	803: "玩乐",
	801: "跳舞",
	805: "游戏",
	811: "娱乐明星",
	810: "城市之声",
}

def getLiveIdsFromCategory(baseUrl="http://webh.huajiao.com/live/listcategory", categoryNo=999, pageCount=8):
	liveIds = set()
	offset = 0
	nums = 20
	kv = {
		"user-agent":"Mizilla/5.0",
		"content-type": "application/json",
	}
	for pageno in range(int(pageCount)+1):
		offset = pageno * nums
		url = baseUrl + "?cateid=%s&offset=%s&nums=%s&fmt=jsonp&_=%s" % (categoryNo, offset, nums, int(time.time()))
		print url
		try:
			resp = requests.get(url=url,headers=kv)
			jsonData = resp.json() # 			jsonData = json.loads(html)
			pp = pprint.PrettyPrinter()
			# pp.pprint(jsonData)
			if jsonData['errno'] != 0:
				continue
			if jsonData['data'] is None:
				continue
			# pp.pprint(jsonData['data']['feeds'])
			ids = set([feed['feed']['relateid'] for feed in jsonData['data']['feeds']])
		except Exception as e:
			print e
			continue
		liveIds |= ids
		#print liveIds
	print "------------------------------------------------------------" + category[categoryNo] + " finished live ids----------------------------------------------------------"
	print len(liveIds)
	# print liveIds
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
	# authorInfo = bsObj.findAll(id="author-info")
	authorInfo = bsObj.findAll("span",class_ ="js-author-id")
	print authorInfo
	res = authorInfo[0].text if authorInfo else ""
	print "UserId: " + res
	return res


# get user data from user page
def getUserData(userId):
	if userId == "":
		return 0
	try:
		html = urlopen("http://www.huajiao.com/user/" + str(userId))
		bsObj = BeautifulSoup(html, "html.parser")
		data = dict()
		userInfoObj = bsObj.find("div", {"id":"userInfo"})
		data['FAvatar'] = userInfoObj.find("div", {"class": "avatar"}).img.attrs['src']
		data['FUserId'] = userId
		#print("data['FUserId']: " + data['FUserId'])
		tmp = userInfoObj.h3.get_text('|', strip=True).split('|')
		print tmp
		print("UserName: " + tmp[0].encode("utf8"))
		data['FUserName'] = tmp[0].encode("utf8")
		tmp = userInfoObj.find("div", {"class": "levels"}).get_text('|', strip=True).split('|')
		data['FLevel'] = tmp[0]
		tmp = userInfoObj.find("ul", {"class":"clearfix"}).get_text('|', strip=True).split('|')
		print tmp
		data['FFollow'] = int(tmp[0].replace(u"万", "")) * 10000 if u"万" in tmp[0].decode("utf-8") else tmp[0]
		data['FFollowed'] = int(tmp[2].replace(u"万", "")) * 10000 if u"万" in tmp[2].decode("utf-8") else tmp[2]
		data['FSupported'] = int(tmp[4].replace(u"万", "")) * 10000 if u"万" in tmp[4].decode("utf-8") else tmp[4]
		data['FExperience'] = int(tmp[6].replace(u"万", "")) * 10000 if u"万" in tmp[6].decode("utf-8") else tmp[6]
		return data
	except AttributeError as e:
		print e
		print(str(userId) + ":html parse error in getUserData()")
		return 0
	except urllib2.HTTPError as e:
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
		# print jsonData['data']['feeds']
		return jsonData['data']['feeds']
	except Exception as e:
		print e
		return 0

def spiderUserDatas(baseUrl="http://webh.huajiao.com/live/listcategory", categoryNo=999, pageCount=8):
	for liveId in getLiveIdsFromCategory(baseUrl, categoryNo, pageCount):
		userId = getUserId(liveId)
		userData = getUserData(userId)
		if userData:
			replaceUserData(userData)
	return 1

def spiderUserLives(nums):
	userIds = selectUserIds(nums)
	for userId in userIds:
		#print userId json data
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
	conn = pymysql.connect(host='localhost', port=3306, user='root', passwd=os.getenv("MYSQL_PASSWORD"), db='huajiaogirls', use_unicode=True, charset='utf8mb4')
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
		cur.execute("SET NAMES utf8mb4;") #or utf8 or any other charset you want to handle
		cur.execute("SET CHARACTER SET utf8mb4;") #same as above
		cur.execute("SET character_set_connection=utf8mb4;") #same as above
		cur.execute("REPLACE INTO Tbl_Huajiao_User(FUserId,FUserName, FLevel, FFollow,FFollowed,FSupported,FExperience,FAvatar,FScrapedTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (int(data['FUserId']), data['FUserName'],int(data['FLevel']),int(data['FFollow']),int(data['FFollowed']), int(data['FSupported']), int(data['FExperience']), data['FAvatar'],getNowTime())
		)
		conn.commit()
	except ValueError as e:
		print("replaceUserData except, userId=" + str(data['FUserId']))
		print data
		print e
	except pymysql.err.InternalError as e:
		print("replaceUserData except, userId=" + str(data['FUserId']))
		print data
		print e
	except UnicodeEncodeError as e:
		print("replaceUserData except, userId=" + str(data['FUserId']))
		print data
		print e

# update user live data
def replaceUserLive(data):
	conn = getMysqlConn()
	cur = conn.cursor()
	try:
		#print(data)
		cur.execute("USE huajiaogirls")
		cur.execute("set names utf8mb4")
		cur.execute("REPLACE INTO Tbl_Huajiao_Live(FLiveId,FUserId,FWatches,FPraises,FReposts,FReplies,FPublishTimestamp,FTitle,FImage,FScrapedTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s )", (int(data['relateid']),int(data['FUserId']), int(data['watches']),int(data['praises']),int(data['reposts']),int(data['replies']),int(data['publishtimestamp']),data['title'], data['image'],getNowTime())
		)
		conn.commit()
	except ValueError as e:
		print("replaceUserLive except, userId=" + str(data['FUserId']))
		print data
		print e
	except pymysql.err.InternalError as e:
		print("replaceUserLive except, userId=" + str(data['FUserId']))
		print data
		print e
	except UnicodeEncodeError as e:
		print("replaceUserLive except, userId=" + str(data['FUserId']))
		print data
		print e

girls = {
	1000: "热门",
	2: "女神",
	999: "校园",
	800: "颜值",
	802: "弹唱",
	801: "跳舞",
	806: "脱口秀",
}

def main(argv):
	if len(argv) < 2:
		print("Usage: python Crawler.py [spiderUserDatas <categoryNo><pageCount> | spiderUserLives <UserIdNums>]")
		exit()
	if (argv[1] == 'spiderUserDatas'):
		baseUrl = "http://webh.huajiao.com/live/listcategory"
		if len(argv) == 3:
			alll = argv[2]
			if alll == "all":
				for cateid, name in category.iteritems():
					if cateid in girls:
						spiderUserDatas(baseUrl, categoryNo=cateid)
			else:
				print("Usage: python Crawler.py [spiderUserDatas <all>|<categoryNo><pageCount>]")
				exit()
		elif len(argv) == 4:
			categoryNo = argv[2]
			pageCount = argv[3]
			spiderUserDatas(baseUrl, categoryNo, pageCount)
		else:
			print("Usage: python Crawler.py [spiderUserDatas <all>|<categoryNo><pageCount>]")
			exit()
		
	elif (argv[1] == 'spiderUserLives'):
		nums = 100
		if len(argv) == 3:
			nums = argv[2]
		elif len(argv) > 3:
			print("Usage: python Crawler.py [spiderUserLives <UserIdNums>]")
			exit()
		spiderUserLives(nums)
	elif (argv[1] == 'getUserCount'):
		print(getUserCount())
	elif (argv[1] == 'getLiveCount'):
		print(getLiveCount())
	else:
		print("Usage: python Crawler.py [spiderUserDatas|spiderUserLives|getUserCount|getLiveCount]")

if __name__ == '__main__':
	main(sys.argv)