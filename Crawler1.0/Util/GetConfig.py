# -*- coding: utf8 -*-

import ConfigParser
import os

class GetConfig(object):
    '''
    get config from config.ini
    '''

    def __init__(self):
        self.pwd = os.path.dirname(os.path.realpath(__file__))
        self.config_path = os.path.join(os.path.dirname(self.pwd), 'Config.ini')
        self.config_file = ConfigParser.ConfigParser()
        self.config_file.read(self.config_path)
        

    def db_type(self):
        return self.config_file.get('DB', 'type')


    def db_name(self):
        return self.config_file.get('DB', 'name')


    def db_host(self):
        return self.config_file.get('DB', 'host')

    def db_port(self):
        return int(self.config_file.get('DB', 'port'))
    