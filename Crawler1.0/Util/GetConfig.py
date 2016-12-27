# -*- coding: utf8 -*-

import ConfigParser
from Util.utilClass import LazyProperty
from Util.utilClass import ConfigParse

import os

class GetConfig(object):
    '''
    get config from Config.ini
    '''

    def __init__(self):
        self.pwd = os.path.dirname(os.path.realpath(__file__))
        self.config_path = os.path.join(os.path.dirname(self.pwd), 'Config.ini')
        self.config_file = ConfigParse()
        self.config_file.read(self.config_path)
        
    @LazyProperty
    def db_type(self):
        return self.config_file.get('DB', 'type')

    @LazyProperty
    def db_name(self):
        return self.config_file.get('DB', 'name')

    @LazyProperty
    def db_host(self):
        return self.config_file.get('DB', 'host')
    @LazyProperty
    def db_port(self):
        return int(self.config_file.get('DB', 'port'))

if __name__ == '__main__':
    gg = GetConfig()
    print gg.__dict__
    print gg.db_type
    print gg.__dict__
    print gg.db_name
    print gg.__dict__
    print gg.db_host
    print gg.__dict__
    print gg.db_port
    print gg.__dict__
