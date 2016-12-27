# -*- coding: utf-8 -*-

import os
import sys
import importlib
import pymysql

from Util.GetConfig import GetConfig

class MysqlClient(object):

    '''
    Mysql Client
    ''' 

    def __init__(self, name, host, port):
        self.name = name
        self.conn = pymysql.connect(host=host, port=port, user='root', passwd='777', db=name, charset='utf8')

    def get(self, **kwargs):
        pass

    def put(self, value, **kwargs):
        pass

    def delete(self, value, **kwargs):
        pass

    def getAll(self):
        pass

    def changeTable(self, name):
        self.name = name