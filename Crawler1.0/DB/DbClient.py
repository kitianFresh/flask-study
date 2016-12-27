# -*- coding: utf8 -*-

import os
import sys
import importlib
from Util.GetConfig import GetConfig

class DbClient(object):

    '''
    DbClient for mutiple database support
    ''' 

    def __init__(self):
        self.config = GetConfig()
        self.__initDbClient()

    def __initDbClient(self):
        __type = None

        if "mysql" == self.config.db_type:
            __type = "MysqlClient"
        else:
            pass
        assert __type, 'type error, Not support Database type: {}'.format(self.config.db_type)

        self.client = getattr(importlib.import_module(__type), __type)(name=self.config.db_name,
                                                                       host=self.config.db_host,
                                                                       port=self.config.db_port)

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