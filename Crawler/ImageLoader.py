# -*- coding: utf-8 -*-

import sys
import os
import urllib2
from urllib2 import urlopen, Request
import pymysql
import cStringIO
try:
	import Image
except ImportError:
	from PIL import Image


def getMysqlConn():
	conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='777', db='huajiaogirls', charset='utf8mb4')
	return conn

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

def getUserCount():
	conn = getMysqlConn()
	cur = conn.cursor()
	cur.execute("USE huajiaogirls")
	cur.execute("set names utf8mb4")
	cur.execute("SELECT count(FUserId) from Tbl_Huajiao_User")
	ret = cur.fetchone()
	return ret[0]

def getUserImageUrl(userId):
	conn = getMysqlConn()
	cur = conn.cursor()
	images = []
	try:
		cur = conn.cursor()
		cur.execute("USE huajiaogirls")
		cur.execute("set names utf8mb4")
		cur.execute("SELECT DISTINCT FImage FROM Tbl_Huajiao_Live WHERE FUserId = %s", (userId))
		ret = cur.fetchall()
		for img in ret:
			#print img
			images.append(img[0])
		#print len(images)
		return images
	except:
		print("getUserImageUrl except")
		return None

def getUserImageUrls(usernum=10):
	images = []
	userIds = selectUserIds(usernum)
	for userId in userIds:
		images.extend(getUserImageUrl(userId[0]))
	return images



def getImage(url):
	'''
	get an resized pil image according to url
	:param url: an image url with an originalName, such as http://image.huajiao.com/4a4fe24f53cd4e2b98480bf4d63c313c.jpg
	:return: a pil image and its originalName,all original images retrieve from url will be resized to 640*640
	'''

	file = cStringIO.StringIO(urlopen(url).read())
	img = Image.open(file)
	exif_data = img._getexif()
	#print img.size, exif_data, url.split('/')[-1]
	originalName = url.split('/')[-1]
	out = img.resize((640,640))
	return out, originalName
	#out.show()
	#img.show()



def saveImage(url, show=False, dir='/home/kinny/Study/Crawler/images/huajiaogirls', size=(1024,1024)):
	'''
	resize the image and save
	'''
	userAgent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36"
	header = {}
	header['User-Agent'] = userAgent
	request = Request(url, headers=header)
	originalName = url.split('/')[-1]
	try:
		resp = urlopen(request)
	except urllib2.URLError as e:
		print "Service Error " + str(e) + "happened when scrapy url: " + url
		return
	file = cStringIO.StringIO(resp.read())
	img = Image.open(file)
	out = img.resize(size)
	if show:
		out.show()
	out.save(os.path.join(dir,originalName))

def spiderAllImages(usernum=10, show=False, dir='/home/kinny/Study/Crawler/images/huajiaogirls'):
	count = 0
	imageUrls = getUserImageUrls(usernum)
	files = os.listdir(dir)
	print "Have scraped images num: " + str(len(files))
	print "Next will scrapy images num: " + str(len(imageUrls)-len(files))

	for imageurl in imageUrls:
		if imageurl.split('/')[-1] in files:
			print("huajiaogirl image: " + imageurl + " have downloaded")
			continue
		count += 1
		saveImage(url=imageurl, show=show)
		print(str(count) + " huajiaogirl image: " + imageurl + " saved to " + dir)
		
		


def main(argv):
	if len(argv) < 2:
		print("Usage: python ImageLoader.py [spiderAllImages <userNums><show:true/false><output>]")
		exit()

	if (argv[1] == 'spiderAllImages'):
		if len(argv) == 2:
			spiderAllImages()
		elif len(argv) == 3:
			nums = argv[2]
			spiderAllImages(nums)
		elif len(argv) == 4:
			nums = argv[2]
			show = True if argv[3] == "true" else False
			spiderAllImages(usernum=nums, show=show)
		elif len(argv) == 5:
			nums = argv[2]
			show = True if argv[3] == "true" else False
			output = argv[4]
			spiderAllImages(usernum=nums, show=show, dir=output)
		else:
			print("Usage: python ImageLoader.py [spiderAllImages <userNums><show:true/false><output>]")
			exit()	
	elif (argv[1] == 'getUserCount'):
		print(getUserCount())
	else:
		print("Usage: python ImageLoader.py [spiderAllImages|getUserCount <userNums><output>]")

if __name__ == '__main__':
	main(sys.argv)