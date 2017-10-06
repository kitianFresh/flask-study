#coding=utf8

from flask import render_template
from flask import Flask, request, Response, jsonify, redirect, json

app = Flask(__name__, static_url_path="")

# 读取配置文件
app.config.from_object('config')

def valid_login(username, password):
    if username == 'hacker' and password == '777':
        return True
    else:
        return False

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if valid_login(request.json['username'],
                       request.json['password']):
           
            return jsonify({"code": 1})
        else:
            return jsonify({"code": -1})
    else:
        return jsonify({"code": -1})


if __name__ == '__main__':
    app.run(host=app.config['SERVER_HOST'], port=app.config['SERVER_PORT'])