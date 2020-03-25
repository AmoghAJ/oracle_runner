#!/usr/bin/python3.6
# __author__ = 'Amogh Jagadale'

import sys

sys.path.append('lib/config-parser')
sys.path.append('lib/oracle-runner')
from oracle_runner import OracleRunner
from config_parser import Config

class Runner:
    
    def __init__(self, enviornment = None):
        self.__config_obj       =   Config(enviornment)
        self.__oracle_runner    =   OracleRunner(self.__config_obj.db_user, 
                                                 self.__config_obj.db_password, 
                                                 self.__config_obj.db_sid, 
                                                 False, 
                                                 self.__config_obj.log_path)
        
    def execute(self, query):
        out = self.__oracle_runner.run(query)
        if out:
            return out
    
    def test_connection(self):
        QUERY = u'SELECT 1 FROM DUAL'
        result = self.execute(QUERY)
        
        if result['data'][0][0] == 1:
            print("Connection Test Succesful.")
            return True
            
        print("Connection Test Failed.")
        return False