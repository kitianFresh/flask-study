
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
### Python 懒加载属性 lazy property
&emsp;&emsp;eager/lazy load/compute/write是计算机系统优化的一个重要技巧（eager还是lazy需要结合场景权衡，他们各有利弊），几乎所有的系统都会出现这个词，包括操作系统，比如虚拟内存中的页面延迟加载，只有当程序真正访问到该页时才会引发页面加载到内存。
也就是某个属性或者数据，初始化或者计算非常耗时，那么系统在未使用他的情况下，就不加载他，直到首次使用才加载，并且缓存起来供以后使用（前提是不再被替换掉）。那么具体到我们写一个类，
类的某个属性我们想实现延迟加载怎么办呢？
&emsp;&emsp;如果你写过Java的单例模式，就会知道其中一种写法就是先声明一个null的成员，然后在实例化中有如下代码，这个可以说就是lazy load 最最简单的模型了。这里就实现了类的实例初始化
时不加载该成员，直到首次使用也就是显式调用时才加载。[java-tip-67--lazy-instantiation](http://www.javaworld.com/article/2077568/learn-java/java-tip-67--lazy-instantiation.html)是一篇关于lazy instanciation in java的文章。
比较麻烦就是，Java中要实现某成员属性的延迟加载，访问必须使用get方法，而不能直接Object.property
``` 
if instance == null
    instance = new instance()
return instance
``` 
Python 中同样，需要对一个类的某些属性进行 lazy load 的话，Python 提供了 @property 的 snytax sugar; 使得我们不用通过方法调用，也能实现访问 lazy property。
```Python
class SomeOtherClass(object):

@property
def calculation_value(self):

    if not hasattr(self, "_calculation_value"):
        self._calculation_value = do_some_big_calculation_or_networks()

    return self._calculation_value

Soc = SomeOtherClass()
Soc.calculation_value
```
```
# -*- coding: utf8 -*-

def some_timing_or_spacing_operation():
    return 6666

class RawLazyClass(object):
    '''
    Java 类似的写法
    '''
    def __init__(self):
        self._lazy_value = None
    @property
    def lazy_value(self):
        if self._lazy_value is None:
            self._lazy_value = some_timing_or_spacing_operation()
        return self._lazy_value


# 这个虽然实现了 Python 方式的 lazy_property， 但是每一次都要重写 属性检查部分。
class AttrLazyClass(object):

    '''
    python 写法
    '''
    def __init__(self):
        pass
    
    @property
    def lazy_value(self):
        # 不能写成 if hasattr(self, '_lazy_value') is None， 返回的是bool:
        if not hasattr(self, '_lazy_value'):
            setattr(self, '_lazy_value', some_timing_or_spacing_operation())
        return getattr(self, '_lazy_value')

# 前面两种写法还有一个缺点就是，必须把 lazy_value 和 函数名字区分开， 否则 AttributeError: can't set attribute，因为 名字一样的话
# 变量就和函数混淆了

# 下面做成decorator之后， 就可以实现通用的 lazy_property 了， 可以减少重复的代码

# 函数版 decorator， 这个本质上和 AttrLazyClass 里的 lazy_value没有区别，如果使用他做装饰器，就是 
# 解释器执行到@lazy_property def lazy_value(self): 时，再一次self.lazy_value = lazy_property(self.lazy_value);实际上还是一个函数
# 只是这个函数被重新定义了，这就是装饰器的魅力所在，装饰器三步走，扔进去，装饰，提出来
def lazy_property(func):
    attr_name = "_" + func.__name__

    @property
    def _lazy_property(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, func(self))
        return getattr(self, attr_name)
    return _lazy_property

class MagicLazyClass(object):

    '''
    Python magic snytax sugar, use decorator
    '''

    def __init__(self):
        pass

    @lazy_property
    def lazy_value(self):
        return some_timing_or_spacing_operation()

# 类版 decorator，这里需要了解什么叫 descriptor, 因为必须要用 descriptor 才能实现类版本的 lazy_property decorator
# 使用这个， 解释器在执行到 @LazyProperty def lazy_value(self): 时，就 执行 self.lazy_value = LazyProperty(self.lazy_value)
# 注意此时，实际上 self.lazy_value本来是函数，现在变成什么了？ 变成了 LazyProperty 类对象了！！！他就是传说中 descriptor
class LazyProperty(object):
    """
    LazyProperty
    """

    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance, self.func.__name__, value)
            return value

class AnotherMagicLazyClass(object):

    '''
    Python magic snytax sugar, use decorator
    '''

    def __init__(self):
        pass

    @LazyProperty
    def lazy_value(self):
        return some_timing_or_spacing_operation()

r = RawLazyClass()
print r.__dict__
print r.lazy_value
print r.__dict__

a = AttrLazyClass()
print a.__dict__
print a.lazy_value
print a.__dict__

m = MagicLazyClass()
print m.__dict__
print m.lazy_value
print m.__dict__

am = AnotherMagicLazyClass()
print am.__dict__
print am.lazy_value
print am.__dict__
```


### data model in python2
 - [Python Data Model](https://docs.python.org/2/reference/datamodel.html)
 - [python-class-attributes-an-overly-thorough-guide](https://www.toptal.com/python/python-class-attributes-an-overly-thorough-guide)
 - [Accessing attributes in Python](http://blog.thedigitalcatonline.com/blog/2015/01/12/accessing-attributes-in-python/#.WFpm-3V97CI)
 - [Introduction to Python: Class 5](http://www2.lib.uchicago.edu/keith/courses/python/class/5/##classinst)
 - [ dictproxyhack, or: ActiveState Code considered harmful](https://eev.ee/blog/2013/08/05/dictproxyhack-or-activestate-code-considered-harmful/##dictproxy)
When you try to access an attribute from an instance of a class, it first looks at its instance namespace. If it finds the attribute, it returns the associated value. If not, it then looks in the class namespace and returns the attribute (if it’s present, throwing an error otherwise)
But when you assign a value to an attribute from a class, with the class's instance.attribute, then it will be dynamically assigned to instance's attribute

### Python descriptor
Python descriptor 的引入，其实是为了让对象的成员变量可以拥有行为；听上去很难懂。成员变量如果是一个对象，那他不就绑定了行为了么。从这个角度解释就直接给初学者一个
很大的门槛。我们以 对象 成员变量需要类型检查为例来解释。
```
>>> class a(object): pass
>>> a.__dict__['wut'] = 4
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'dictproxy' object does not support item assignment
>>> setattr(a, 'wut', 7)
>>> a.wut
7
```
#### 参考
 - [Python Descriptors Demystified](http://nbviewer.jupyter.org/urls/gist.github.com/ChrisBeaumont/5758381/raw/descriptor_writeup.ipynb)
 - [Classes and Objects II: Descriptors](http://intermediatepythonista.com/classes-and-objects-ii-descriptors)
 - [Decorators and Descriptors](http://www.ianbicking.org/blog/2008/10/decorators-and-descriptors.html)



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