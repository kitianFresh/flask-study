# flaskr 开发笔记

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
