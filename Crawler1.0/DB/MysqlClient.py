# -*- coding: utf-8 -*-

import os
import sys
import importlib
import pymysql

from Util.GetConfig import GetConfig

class DbClient(object):

    '''
    DbClient for mutiple database support
    ''' 

    def __init__(self):
        self.config = GetConfig()
        self.conn = 

    def get(self, **kwargs):
        return self.client.get(**kwargs)

    def put(self, value, **kwargs):
        return self.client.put(value, **kwargs)

    def delete(self, value, **kwargs):
        return self.client.delete(value, **kwargs)

    def getAll(self):
        return self.client.getAll()

    def changeTable(self, name):
        self.client.changeTable(name)