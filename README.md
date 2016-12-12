# Flask Study Notes

### Requirements
 - python 2.7
 - Flask
 - mongoDB
 - pymongo

### Flask web框架安装
安装[Flask](http://flask.pocoo.org/docs/0.11/quickstart/)
```
pip install Flask
```
### Mongodb 安装
安装[mongoDB](https://docs.mongodb.com/manual/installation/)
```
// ubuntu 16.04
echo "deb http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list
// ubuntu 14.04
echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list

//国外repo直接安装太慢，因此这里把你的Ubuntu软件源更换为aliyun或者中科大的。
//将上面的 http://repo.mongodb.org 更换为 http://mirrors.aliyun.com/mongodb
echo "deb http://mirrors.aliyun.com/mongodb/apt/ubuntu xenial/mongodb-org/3.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list

sudo apt-get update
sudo apt-get install -y mongodb-org
sudo service mongodb started
sudo mongo

```

#### 参考
 - [官网](https://docs.mongodb.com/manual/installation/)
 - [install-mongodb-on-ubuntu-16.04](https://www.howtoforge.com/tutorial/install-mongodb-on-ubuntu-16.04/)

#### 国外镜像安装过慢的方法
 - [Ubuntu16.04使用阿里云镜像安装Mongodb](http://www.linuxdiyf.com/linux/26151.html)

### Mongodb的python客户端开发
安装[python driver](https://docs.mongodb.com/getting-started/python/client/)
```
pip install pymongo
```

# repo fork notes

 - [fork-a-repo](https://help.github.com/articles/fork-a-repo/)
 - [syncing-a-fork](https://help.github.com/articles/syncing-a-fork/)
 - [creating-a-pull-request](https://help.github.com/articles/creating-a-pull-request/)


# flaskr 开发笔记

## Python 虚拟环境使用
虚拟环境很好使，推荐使用，他不会影响你的Ubuntu自带的Python环境，相当于重新创建了一个Python环境，然后在这个环境下进行包的安装和开发！以下是简单的安装和使用方法

```
// 可能没得virtaualenv，先安装
sudo apt-get install python-pip python-dev python-virtualenv
// 然后新建一个目录,比如你的项目
mkdir todo-api
cd todo-api
// 该句会创建一个flask目录，就是一个新的Python虚拟环境，里面的目录结构其实和主机上Python目录结构很类似，都有bin目录下的命令，比如pip，python，activate等
virtualenv flask
//然后你可以使用flask/bin/pip安装项目需要的依赖包，此时安装的就是Flask包了，他在flask/lib/python2.7/site-packages目录下面，不会影响local Python的。
flask/bin/pip install flask
//如果你想要运行.py文件，可以直接使用
flask/bin/python app.py
//当然还可以使用
chmod a+x app.py
./app.py

```
## web app 配置方式
>Flask allows you to import multiple configurations and it will use the setting defined in the last import. 
从文件导入配置

```python
app.config.from_pyfile(filename, silent=False)
```
从对象导入配置

```python
app.config.from_object(obj)
	obj: string, 叫这个名字的模块会被import,也可以是一个直接已经导入的object
```
从环境变量指定的地方导入

```python
app.config.from_envvar(variable_name, silent=False)
```
从一个词典导入，运行时更新

```python
app.config.update(dict)
```

## flask 引入上下文的概念
为了保证同一个请求共享数据库连接，而不是反复connect_db(),flask引入applocation context的概念，g 是全局共享的

```python
def get_db():
	"""Opens a new database connection if there is none yet for the
    current application context.
    """
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db
```

## flask 提供命令行接口，并可以读取APP资源
```
def init_db():
	db = get_db()
	with app.open_resource('schema.sql', mode='r') as f:
		db.cursor().executescript(f.read())
	db.commit()
# flask的命令行接口创建数据库
@app.cli.command('initdb')
def initdb_command():
	init_db()
	print 'Initialized the database.'
```

# 爬虫笔记

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