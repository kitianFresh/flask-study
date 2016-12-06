#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
from flask import Flask, request, Response, render_template, jsonify, abort, make_response
from werkzeug.utils import secure_filename
from pymongo import MongoClient
import bson
from cStringIO import StringIO
from PIL import Image

from imageFilter import ImageFilter
import cv2
import numpy
import json
from bson.json_util import dumps


app = Flask(__name__, static_url_path="")
# 读取配置文件
app.config.from_object('config')
# 连接数据库，并获取数据库对象
db = MongoClient(app.config['DB_HOST'], app.config['DB_PORT']).test


def save_file(content, name):

	# content = StringIO(f.read())
	try:
		mime = Image.open(content).format.lower()
		if mime not in app.config['ALLOWED_EXTENSIONS']:
			raise IOError()
	except IOError:
		abort(400)
	c = dict(content=bson.binary.Binary(content.getvalue()),
	         filename=secure_filename(name), mime=mime)
	db.files.save(c)
	return c['_id'], c['filename']


@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template("upload.html")


@app.route('/upload', methods=['POST'])
def upload():
	if request.method == 'POST':
		if 'imagefile' not in request.files:
			abort(400)
		imgfile = request.files['imagefile']
		if imgfile.filename == '':
			abort(400)
		if imgfile:
			# pil = StringIO(imgfile)
			# pil = Image.open(pil)
			img = cv2.imdecode(numpy.fromstring(
			    imgfile.read(), numpy.uint8), cv2.CV_LOAD_IMAGE_UNCHANGED)
			if img is None:
				return jsonify({"error": "please make sure your picture is perfect"})
			filtered = ImageFilter(image=img).filter()
			if filtered is None:
				return jsonify({"error": "please make sure your picture is perfect"})
			content = StringIO()
			filtered.save(content, format="JPEG")
			fid, filename= save_file(content,imgfile.name)
			print(fid)
			templates = "<div><img id=\'filtered-report\' src=\'/file/%s\' class=\'file-preview-image\' width=\'100%%\' height=\'512\'></div>"%(fid)
			data = {
				"templates": templates
			}
			return jsonify(data)
        abort(400)

'''
	根据图像oid，在mongodb中查询，并返回Binary对象
'''
@app.route('/file/<fid>')
def find_file(fid):
	try:
		file = db.files.find_one(bson.objectid.ObjectId(fid))
		if file is None:
			raise bson.errors.InvalidId()
		return Response(file['content'], mimetype='image/' + file['mime'])
	except bson.errors.InvalidId:
		flask.abort(404)

'''
	根据报告oid，抽取透视过得图像，然后进行OCR，并返回OCR结果
'''
@app.route('/report/<fid>')
def get_report(fid):
	try:
		file = db.files.find_one(bson.objectid.ObjectId(fid))
		if file is None:
			raise bson.errors.InvalidId()
		print(type(file['content']))
		
		img = cv2.imdecode(numpy.fromstring(dumps(file['content']), numpy.uint8), cv2.CV_LOAD_IMAGE_UNCHANGED)
		report_data = ImageFilter(image=img).ocr(22)
		print report_data
		if report_data is None:
			return jsonify({"error": "can't ocr'"})
		return jsonify(report_data)
	except bson.errors.InvalidId:
		flask.abort(404)

if __name__ == '__main__':
    app.run(host=app.config['SERVER_HOST'],port=app.config['SERVER_PORT'])
