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

### Deploy

# repo fork notes

[fork-a-repo](https://help.github.com/articles/fork-a-repo/)
[syncing-a-fork](https://help.github.com/articles/syncing-a-fork/)
[creating-a-pull-request](https://help.github.com/articles/creating-a-pull-request/)


# flaskr 开发笔记

## Python 虚拟环境使用
虚拟环境很好使，推荐使用，他不会影响你的Ubuntu自带的Python环境，相当于重新创建了一个Python环境，然后在这个环境下进行包的安装和开发！以下是简单的安装和使用方法

```
// 可能没得virtaualenv，先安装
sudo apt-get install python-pip python-dev python-virtualenv
// 然后新建一个目录
```
## web app 配置方式
Flask allows you to import multiple configurations and it will use the setting defined in the last import. 
从文件导入配置
app.config.from_pyfile(filename, silent=False)
从对象导入配置
app.config.from_object(obj)
	obj: string, 叫这个名字的模块会被import,也可以是一个直接已经导入的object
从环境变量指定的地方导入
app.config.from_envvar(variable_name, silent=False)
从一个词典导入，运行时更新
app.config.update(dict)

## flask 引入上下文的概念
为了保证同一个请求共享数据库连接，而不是反复connect_db(),flask引入applocation context的概念，g 是全局共享的
```
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