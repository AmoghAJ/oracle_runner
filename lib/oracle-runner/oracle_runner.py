#!//usr/bin/python3.6
# __author__ = 'Amogh Jagadale'

from __future__ import print_function
import sys
import cx_Oracle
import logging
import os
from datetime import datetime

class OracleRunner:
    
    DEFAULT_LOG_LEVEL = logging.INFO
    
    def __init__(self, user, password, sid, print_query_stdout = False, log_path = None):
        self.__user                 =   user
        self.__password             =   password
        self.__sid                  =   sid
        self.__return_output        =   False
        self.__commit               =   False
        self.__print_query_stdout   =   print_query_stdout
        self.__log_filename         =   self._get_log_path(log_path)
        self.__blacklisted_tables   =   self._get_blacklisted_tables()
        self._set_logging()

    def _get_log_path(self, log_path):
        if not log_path:
            log_path = "logs"
        
        return os.path.join(log_path, "%s-oracle-runner.log"%str(datetime.today().strftime('%Y%m%d-%H%M%S')))
            
    def _set_logging(self):
        logging.basicConfig(filename=self.__log_filename,
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level= self.DEFAULT_LOG_LEVEL)
    
    @property
    def _masked_connecton_str(self):
        connection_str = "%s/%s@%s"%(self.__user, "*"*len(self.__password), self.__sid)
        return connection_str
    
    def _get_blacklisted_tables(self):
        f = open('blacklisted_tables', 'r')
        black_listed_tables = f.readlines()
        f.close()
        return black_listed_tables
    
    def _open(self):
        con_str = u"%s/%s@%s"%(self.__user, self.__password, self.__sid)
        
        try:
            cnx = cx_Oracle.connect(con_str)
            self.__connection   =   cnx
            logging.info("Connection established to the database. connection string: %s"%self._masked_connecton_str)
        except Exception as e:
            print("Error in establishing the connection to the database.")
            logging.critical("Failed to connect to database. connection string: %s"%self._masked_connecton_str, exc_info = True)
            sys.exit(1)
        
        try:
            self.__session      =   cnx.cursor()
            logging.info("Database cursor created.")
        except Exception as e:
            print("Something went wrong while opening connection to the database")
            logging.critical("Failed to create database cursor",exc_info = True)
            self.__connection.close()
            sys.exit(1)
       
    def _close(self):
        try:
            self.__session.close()
            logging.info("database cursor destroyed.")
            self.__connection.close()
            logging.info("database connection closed.")
        except Exception as e:
            logging.error("Unable to destroy cursor and close database connection", exc_info = True)
            
    
    def _commit_required(self, query_header):
        commit_for_headers = ['update', 'insert', 'delete', 'drop']       
        if query_header in commit_for_headers:
            self.__commit = True
            logging.info("Query header: %s, Commit required: True"%query_header)

    def _is_select_query(self, query_header):
        if query_header == 'select':
            self.__return_output = True
            logging.info("Query header: %s, Return output: True"%query_header)
    
    def _commit(self):
        try: 
            self.__connection.commit()
            logging.info("Successfuly commited.")
        except Exception as e:
            logging.error("Falied to perform commit.", exc_info = True)
    
    def _get_result(self):
        try:
            result = self.__session.fetchall()
            if result:
                columns_desc = self.__session.description
                columns = [i[0] for i in columns_desc]
                logging.info("Data succesfully fetched from database.")
                return {"header": columns, "data": result}
        except Exception as e:
            logging.error("Falied to fetch data.", exc_info = True)
        
    def _black_list_verification(self, query):
        for table in self.__blacklisted_tables:
            if table.lower() in query.lower():
                print("Query execution is prohibited on table: %s" %table)
                logging.error("Attempt of query execution on Blacklisted table is observered. Query: %s"%query)
                sys.exit(1)
    
    def run(self, query):
        result = None
        
        self._black_list_verification(query)
        query_header = query.split(' ', 1)[0].lower()
        self._commit_required(query_header)
        self._is_select_query(query_header)
        
        self._open()
        
        try:
            self.__session.execute(query)
            logging.info("Query executed: %s" %query)
            
        except Exception as e:
            print("Query execution falied, please verify if the SQL query is correct.")
            logging.error('Query execution failed, Query: %s'%query, exc_info = True)
            self._close()
            sys.exit(1)
        
        if self.__print_query_stdout:
            print("Query: '%s' executed succesfully."%query)
        
        if self.__commit:
            self._commit()
        
        if self.__return_output:
            result = self._get_result()
            self._close()
            return result

        self._close()