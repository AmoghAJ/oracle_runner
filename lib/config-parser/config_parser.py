#!/usr/bin/python3.6
# __author__ = 'Amogh Jagadale'

from __future__ import print_function
import os
import sys
import configparser

sys.path.append('../../')

class Config:
    
    CONFIG_FILE = os.path.join("conf","configuration.ini")

    
    def __init__(self, enviornment = None):
        self.__parser_obj       =   configparser.ConfigParser()
        self.__parser_obj.read(self.CONFIG_FILE)
        self.__enviornment       =  enviornment if enviornment else self.__parser_obj.get("environment", "default")
        self.__config_file_path  =  self.__parser_obj.get("config-file-path", self.__enviornment)
        self.__config_content    =  self.parse_plain_text_config()
        self.__username_header   =  self.__parser_obj.get("default-config-headers", "USERNAME_CONFIG_HEADER")
        self.__password_header   =  self.__parser_obj.get("default-config-headers","PASSWORD_CONFIG_HEADER")
        self.__sid_header        =  self.__parser_obj.get("default-config-headers", "SID_CONFIG_HEADER")
        self.__log_path          =  self.__parser_obj.get("log-path", "default")
    
    def parse_plain_text_config(self):
        f = open(self.__config_file_path)
        config_content = f.readlines()
        
        config = {}
        for each_line in config_content:
            property_line = each_line.split('=')
            config[property_line[0]] = property_line[1].rstrip()
        
        return config

    @property
    def db_user(self):
        return self.__config_content[self.__username_header]
    
    @property
    def db_password(self):
        return self.__config_content[self.__password_header]

    @property
    def db_sid(self):
        return self.__config_content[self.__sid_header]

    @property
    def log_path(self):
        if self.__log_path == 'None':
            return None
        
        return self.__log_path