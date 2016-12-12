import urllib  
import urllib2  
 
url = 'http://www.zhihu.com/#signin'
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'  
values = {'username' : '13237102479@163.com',  'password' : 'zhihu777tianqi' }  
headers = { 'User-Agent' : user_agent }  
data = urllib.urlencode(values)  
request = urllib2.Request(url, data, headers)
try:
	response = urllib2.urlopen(request)
except urllib2.HTTPError, e:
	print e.code
except urllib2.URLError, e:
	print e.reason
else:
	print "OK"
page = response.read() 

import pymysql

conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='777', db='huajiaogirls', charset='utf8mb4')

print conn.cursor()