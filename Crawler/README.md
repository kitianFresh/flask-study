
# 爬虫笔记

## 注意
### Python 中的 file.name 
file.name是包含整个传递进来的路径的，如果仅仅想要获得文件的名字，使用os.path.basename(file.name)
### pymysql 中 fetchall() 
返回的是 an array of tuple，即一条条记录的集合，you need for e in arr e[0] e[1] e[2]... to access
### PIL 中对 Image draw 之后进行 image.save，会毁坏原始图像
use another copy of original image , or the draw operation will destroy original one if you save
### 包导入错误
```Python
root = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root)
```
### POST 提交带文件数据的表单
参考: [四种常见的 POST 提交数据方式](https://imququ.com/post/four-ways-to-post-data-in-http.html);[rfc1867](http://www.ietf.org/rfc/rfc1867.txt)
```Python
# reference: http://www.learntosolveit.com/python/web_urllib2_binary_upload.html
import os
import urllib2
import itertools
import mimetools
import mimetypes
from cStringIO import StringIO
import urllib
import urllib2
import json
import sys
_width = len(repr(sys.maxsize-1))
_fmt = '%%0%dd' % _width

def _make_boundary():
    # Craft a random boundary.
    token = random.randrange(sys.maxsize)
    boundary = ('=' * 15) + (_fmt % token) + '=='
    return boundary

class MultiPartForm(object):
    """Accumulate the data to be used when posting a form."""

    def __init__(self):
        self.form_fields = []
        self.files = []
        self.boundary = mimetools.choose_boundary()
        return
    
    def get_content_type(self):
        return 'multipart/form-data; boundary=%s' % self.boundary

    def add_field(self, name, value):
        """Add a simple field to the form data."""
        self.form_fields.append((name, value))
        return

    def add_file(self, fieldname, filename, fileHandle, mimetype=None):
        """Add a file to be uploaded."""
        body = fileHandle.read()
        if mimetype is None:
            mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        self.files.append((fieldname, filename, mimetype, body))
        return
    
    def __str__(self):
        """Return a string representing the form data, including attached files."""
        # Build a list of lists, each containing "lines" of the
        # request.  Each part is separated by a boundary string.
        # Once the list is built, return a string where each
        # line is separated by '\r\n'.  
        parts = []
        part_boundary = '--' + self.boundary
        
        # Add the form fields
        # 参数是一个列表元素构成的列表
        parts.extend(
            [ part_boundary,
              'Content-Disposition: form-data; name="%s"' % name,
              '',
              value,
            ]
            for name, value in self.form_fields
            )
        
        # Add the files to upload
        parts.extend(
            [ part_boundary,
              'Content-Disposition: file; name="%s"; filename="%s"' % \
                 (field_name, filename),
              'Content-Type: %s' % content_type,
              '',
              body,
            ]
            for field_name, filename, content_type, body in self.files
            )
        
        # Flatten the list and add closing boundary marker,
        # then return CR+LF separated data
        # itertools.chain(*parts) 是对列表的列表的递归拆解成单个元素的列表
        flattened = list(itertools.chain(*parts))
        flattened.append('--' + self.boundary + '--')
        flattened.append('')
        return '\r\n'.join(flattened)
```



## 坑爹的Fiddler
千万不要装Fiddler，这个东西在Ubuntu下面不好使，基本上好多包都监听不了，而且还修改你的系统代理配置，导致我的wget curl一切网络有关的命令都无法使用了！真是坑爹啊！解决办法之一是暴力改回System wide proxy settings，可以参考[change-system-proxy-settings-command-line-ubuntu-desktop](http://ask.xmodulo.com/change-system-proxy-settings-command-line-ubuntu-desktop.html)，下面都是入坑之后的结果，都不能正常使用了。
```
kinny@kinny-Lenovo-XiaoXin:~$ curl https://www.youtube.com
curl: (7) Failed to connect to 127.0.0.1 port 8888: Connection refused

kinny@kinny-Lenovo-XiaoXin:~$ proxychains curl https://www.youtube.com
ProxyChains-3.1 (http://proxychains.sf.net)
curl: (56) Proxy CONNECT aborted

kinny@kinny-Lenovo-XiaoXin:~$ wget https://www.charlesproxy.com/assets/release/4.0.2/charles-proxy-4.0.2.tar.gz
--2016-12-06 11:33:38--  https://www.charlesproxy.com/assets/release/4.0.2/charles-proxy-4.0.2.tar.gz
Connecting to 127.0.0.1:8888... failed: Connection refused.

kinny@kinny-Lenovo-XiaoXin:~$ proxychains wget https://www.charlesproxy.com/assets/release/4.0.2/charles-proxy-4.0.2.tar.gz
ProxyChains-3.1 (http://proxychains.sf.net)
--2016-12-06 11:33:47--  https://www.charlesproxy.com/assets/release/4.0.2/charles-proxy-4.0.2.tar.gz
Connecting to 127.0.0.1:8888... connected.
Failed reading proxy response: Success
Retrying.

--2016-12-06 11:33:48--  (try: 2)  https://www.charlesproxy.com/assets/release/4.0.2/charles-proxy-4.0.2.tar.gz
Connecting to 127.0.0.1:8888... connected.
Failed reading proxy response: Success
Retrying.

^C
```

## uninstall mono
参考：[how-to-permanently-remove-all-mono-related-package-libs-apps-etc](http://unix.stackexchange.com/questions/2035/how-to-permanently-remove-all-mono-related-package-libs-apps-etc)


## 关键点
 1. 爬虫要定时执行，对于已经采集到的数据，采取何种更新策略
 2. 直播历史数据需要请求相应的ajax接口，对收到的数据进行json解码分析
 3. 主播昵称包含emoji表情，如果数据库使用常用的编码”utf8″则会写入报错
 4. 过滤直播地址来获取直播id时，需要使用到正则匹配，我使用的是Python库”re”
 5. 分析html，我使用的是”BeautifulSoup”
 6. 读写mysql，我使用的是”pymysql”

## 技巧
 1. 没有使用mysql的“INSERT”，而是使用了“REPLACE”,是当包含同样的FUserId的一条记录被写入时将替换原来的记录，这样能够保证爬虫定时更新到最新的数据。
 2. Tbl_Huajiao_Live用于存储主播的历史直播数据，其中字段FScrapedTime是每次记录更新的时间，依靠此字段可以实现简单的更新策略。

## 错误
1.
```
File "/usr/local/lib/python2.7/dist-packages/pymysql/connections.py", line 659, in __init__
    self.encoding = charset_by_name(self.charset).encoding
AttributeError: 'NoneType' object has no attribute 'encoding'

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='XXX', db='huajiaogirls', charset='utf-8')
```
改为charset='utf-8'

2.
```
{"errno":0,"msg":"","data":[]}没有对这种返回处理，没有错误，只是没有直播历史而已
```

3. UserId 解析总是会包含错误，原因是这个，有些title 中名字里包含数字，导致解析错误,列如下面的;方案有两种，直接更换解析Title的正则，先识别出ID:XXX,在拿出XXX； 另一种可以不从Title标签里选择，可以从另一个地方，<div id="author-info"></div>里面拿出来
```Python
Text: 【怼+01】💖萌哒哒✨甜甜圈💖正在直播《Ccccccccc》，ta的花椒ID:33412388，快来关注吧 - 花椒直播,美颜椒友,疯狂卖萌
UserId: 01 
#res = re.findall("[0-9]+", text)
#print "UserId: " + res[0]
'NoneType' object has no attribute 'find'
01:html parse error in getUserData()

```
采用第一种，又发现这样的；因此为了保险，还是采用Html元素里的比较保险，格式比较统一， Title里是字符串拼接出来的，可能格式有点不一样
```
Text: 叫我阿佳吖正在直播,ta的花椒id:81425289,快来关注吧 - 花椒直播,美颜椒友,疯狂卖萌
```


## utf8mb4可以让MySql支持emoji，方案之一是采用utf8mb4编码
在创建数据库和表格的时候，采用此编码,然后在连接数据库的时候也制定该编码
```
DROP DATABASE IF EXISTS `huajiaogirls`;
CREATE DATABASE `huajiaogirls` DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_general_ci;
USE `huajiaogirls`;
set names utf8mb4;

DROP TABLE IF EXISTS `Tbl_Huajiao_Live`;
CREATE TABLE `Tbl_Huajiao_Live` (
    `FLiveId` INT UNSIGNED NOT NULL,
    `FUserId` INT UNSIGNED NOT NULL,
    `FWatches` INT UNSIGNED NOT NULL DEFAULT 0  COMMENT '观看人数',
    `FPraises` INT UNSIGNED NOT NULL DEFAULT 0  COMMENT '赞数',
    `FReposts` INT UNSIGNED NOT NULL DEFAULT 0  COMMENT 'unknown',
    `FReplies` INT UNSIGNED NOT NULL DEFAULT 0  COMMENT 'unknown',
    `FPublishTimestamp` INT UNSIGNED NOT NULL COMMENT '发布日期',
    `FTitle` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '直播名称',
    `FImage` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '直播封面',
    `FLocation` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '地点',
    `FScrapedTime` timestamp NOT NULL COMMENT '爬虫更新时间',
    PRIMARY KEY (`FLiveId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

```
 - [让MySQL支持emoji表情符号存储](http://www.hi-linux.com/2016/03/28/%E8%AE%A9MySQL%E6%94%AF%E6%8C%81emoji%E8%A1%A8%E6%83%85%E7%AC%A6%E5%8F%B7%E5%AD%98%E5%82%A8/)
 - [Emoji表情符号在MySQL数据库中的存储](http://www.jianshu.com/p/20740071d854)

## 瑕疵
```
replaceUserData except, userId=76270958
replaceUserData except, userId=55518755
replaceUserData except, userId=28740588
replaceUserData except, userId=21398501
replaceUserData except, userId=25241354
replaceUserData except, userId=56930235
replaceUserData except, userId=54599384
replaceUserData except, userId=83262321
replaceUserData except, userId=75036102

'decimal' codec can't encode characters in position 2-4: invalid decimal Unicode string
'decimal' codec can't encode character u'\U0001f412' in position 0: invalid decimal Unicode string

UserId: uid
'NoneType' object has no attribute 'find'
uid:html parse error in getUserData()
```

## 变换user agent

### 应用部署和安装
安装依赖
```
pip -r install requirements.txt
```
建立MySQL数据库
```
mysql -uroot -p < schema.sql
```
启动
```
先启动以下文件爬取用户信息
python Crawler.py spiderUserDatas
再启动以下命令从已经爬取到的user信息爬取每个User的live信息，这里面会有合适的图片
python Crawler.py spiderUserLives
该文件用于下载真实的图片，图片url从MySQL读取
python ImageLoader.py spiderAllImages
最后过滤并标记带人脸的照片，特征点存储到MySQL，标记后的图片存储到本地文件系统
python FaceFilter.py
```
