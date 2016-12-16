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


# Python Deeplearning 杂记
# Python dump/dumps,load/loads
## JSON (JavaScript Object Notation)
&emsp;&emsp;JSON是一种文件格式，同时也是JavaScript中的对象，JSON在python中的对应数据结构是dict.
 1. dump, 将一个python dict/list object 转换为JSON object，这样就可以写入文件或者用于网络传输
 2. load, 将一个JSON object 转换为python object(dict/list)，这样就可以在python程序中方便使用

## dump，load 与dumps，loads的区别
 1. dump,load用于处理file objects
 2. dumps, loads用于处理string object自己

## code examples:
### writing dict to JSON file and reading JSON file to dict
```python
import json

# writing dict to JSON file
pythondict = {
    'name': 'kinny',
    'age': 1000,
    'skills': ['programmer', 'musician', 'painter']
}

with open("file.json", 'w') as outfile:
    json.dump(pythondict, outfile, indent=4)
    # indent =4 is for indenting the json aka pretty printing but will need more space because spaces fill

# reading JSON file to dict    
jsonfile = open("file.json", 'r')
jsondict = json.load(jsonfile)
print(type(jsondict))
# the 'jsondict' is a python dict object
jsonfile.close()
```

### writing dict to JSON string and reading JSON string to dict
```python
import json

'''
Python 3 with aiohttp package.
'''
# reading a JSON string to dict
jsonstring = '{"name": "kinny", "age": 1000, "skills" : ["programmer", "musician", "painter"]}'

pdict = json.loads(jsonstring)
print(type(pdict))
print(pdict)

# write a python dict/list to JSON string
print(json.dumps(pdict))


# networks json data trainsition
# web.Response(status=response_code,body=json.dumps(response).encode('utf-8'),content_type='application/json',charset='utf-8')

```

# 安装图像处理模块

```
sudo pip install Pillow
//tesseract-ocr库
sudo apt-get install tesseract-ocr
// tesseract-ocr pthon wrapper
sudo pip install pytesseract

//tesseract-ocr默认没有中文字符集，下载中文字符集
wget https://github.com/tesseract-ocr/tessdata/raw/master/chi_sim.traineddata

//然后copy到目录/usr/share/tesseract-ocr/tessdata/
sudo cp chi_sim.traineddata /usr/share/tesseract-ocr/tessdata/

//example
from PIL import Image
import pytesseract
print(pytesseract.image_to_string(Image.open('血常规.jpg'), lang='chi_sim'))

```
## 安装Python机器视觉编程[英文](http://programmingcomputervision.com/)[中文](http://yongyuan.name/pcvwithpython/)中PCV库
依赖
```
sudo pip install numpy
sudo pip install matplotlib
sudo pip install scipy

```
[下载库到本地](https://github.com/jesolem/PCV/zipball/master)
```
cd jesolem-PCV-376d597/
sudo python setup.py install

//以下命令可以用来确定Ubuntu系统拥有的字体和位置
fc-list :lang=zh 

import PCV
```

## 参考
 - [基本的图像处理与 OCR 文字识别工具总结 (Python)](https://testerhome.com/topics/4615)

# 安装VScode
1.下载[压缩包](https://code.visualstudio.com/Download)code-stable-code_1.7.2-1479766213_amd64.tar.gz
```
cd Download

//解压到/opt目录
sudo tar -xzf code-stable-code_1.7.2-1479766213_amd64.tar.gz -C /opt

//创建VSCode软连接，目的是方便以后更换新版本VSCode就不用配置了，直接替换当前的VSCode-linux-x64
sudo ln -s /opt/VSCode-linux-x64/ /opt/VSCode

//创建运行的软连接，这样就可以在任意目录运行code,其实可以直接进入VSCode-linux-x64目录下面运行code，
//或者直接配置环境变量，以下配置是为了保持系统环境变量的干净整洁
//这里因为/usr/local/bin默认总是在环境变量中，所以下载的软件都可以这样做，
sudo ln -s /opt/VSCode/code /usr/local/bin/code

code .
```
2.可以配置桌面快捷方式，编辑文件： sudo vi /usr/share/applications/VSCode.desktop
```
#!/usr/bin/env xdg-open

[Desktop Entry]
Version=1.7.2
Type=Application
Terminal=false
Exec=/opt/VSCode/code
Name=VSCode
Icon=/opt/VSCode/resources/app/resources/linux/code.png
Categories=Development
```

# 实现图片上传到服务器并写入mongodb
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
fast tutorial
```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import MongoClient

# CRUD
# create
# 1. create a connection
client = MongoClient("mongodb://localhost:27017")
#default connect to mongodb://localhost:27017
#client = MongoClient()

# 2. access database objects, remote database object assign to local db
db = client.test
#db = client['test'] dictionary-style

# 3. access collection objects
coll = db.restaurants
#coll = db['restaurants']



# update
from datetime import datetime
'''Python
The operation returns an InsertOneResult object, 
which includes an attribute inserted_id that contains the _id of the inserted document. 
Access the inserted_id attribute:

result = coll.insert_one(
    {
        "address": {
            "street": "2 Avenue",
            "zipcode": "10075",
            "building": "1480",
            "coord": [-73.9557413, 40.7720266]
        },
        "borough": "Manhattan",
        "cuisine": "Italian",
        "grades": [
            {
                "date": datetime.strptime("2014-10-01", "%Y-%m-%d"),
                "grade": "A",
                "score": 11
            },
            {
                "date": datetime.strptime("2014-01-16", "%Y-%m-%d"),
                "grade": "B",
                "score": 17
            }
        ],
        "name": "Vella",
        "restaurant_id": "41704620"

    }
)
print(result.inserted_id)
'''

# read
# query by a top level field
cursor = db.restaurants.find({"borough": "Manhattan"})
for document in cursor:
    print(document)

# query by a field in an embedded document,use dot notation
cursor = db.restaurants.find({"address.zipcode": "10075"})
for document in cursor:
    print(document)
```

# javascript新手掉坑指南

## Python后台如果传回HTML文本，那么HTML文本需要转义字符转义

```
"initialPreview": "<img src=\'/file/{0}\' class=\'file-preview-image\' style=\'width:100%\'>".format(fid)
"initialPreview": "<img src=\'/file/%s\' class=\'file-preview-image\' style=\'width:100%%\'>"%(fid)
```
## JQuery element.show()不起作用，和css有关
[jQuery show() for Twitter Bootstrap css class hidden](http://stackoverflow.com/questions/14610412/jquery-show-for-twitter-bootstrap-css-class-hidden)

## JQuery 表单提交后监听事件处理
[Sending multipart/formdata with jQuery.ajax](http://stackoverflow.com/questions/5392344/sending-multipart-formdata-with-jquery-ajax)
```javascript
首先对表单元素进行submit监听，回调函数中使用$.ajax自己传输数据，
但是对要传输的数据使用new FromData(this)
$(document).on('submit', "form#data", function(e) {
        e.preventDefault();
        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: new FormData(this),
            processData: false,
            contentType: false
        }).done(function(data) {
            console.log(data.templates);
            $("#filtered-image").empty().append(data.templates);
        });

});
```

## JQuery 动态增删改除元素或内容
当select内容本身为空时，直接调用add不起作用，应该用append，因为不一定支持add方法，w3school是最权威的，里面并没有add方法，但是有的jQuery文档可能有
```
empty() will remove all the contents of the selection.
remove() will remove the selection and its contents.
```
## JQuery “Uncaught SyntaxError: Unexpected token o”
[i-keep-getting-uncaught-syntaxerror-unexpected-token-o](http://stackoverflow.com/questions/8081701/i-keep-getting-uncaught-syntaxerror-unexpected-token-o)
```
 jQuery takes a guess about the datatype. It does the JSON parsing even though you're not calling getJSON()
Basically if the response header is text/html you need to parse, and if the response header is application/json it is already parsed for you.
```
## vue.js 访问model data的方式
```
var vm = new Vue({
  data:{
  a:1
  }
})
// `vm.a` 是响应的
vm.b = 2
```

## Git出现merge或者pull与本地工作区状态冲突
```
Updating c5ba2bc..ad63656
error: Your local changes to the following files would be overwritten by merge:
    BloodTestReportOCR/static/index.html
    BloodTestReportOCR/view.py
Please, commit your changes or stash them before you can merge.
Aborting
```

方案1： git stash，他会把当前工作区的保存到一个Git栈中,当需要取出来的时候，git stash pop会从Git栈中读取最近一次保存的内容，恢复工作区的相关内容
```
git stash
git merge

git stash list： 所有保存的git栈内的备份
git stash pop： 弹出栈顶内容
git stash clear： 清空Git栈
```
方案2：放弃本地修改就可以了
```
git reset --hard
git pull
```