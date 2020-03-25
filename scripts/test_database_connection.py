#!/usr/bin/python3.6
# __author__ = 'Amogh Jagadale'
import sys
import argparse

from enviornment_setter import set_enviornment
set_enviornment()

from main import Runner

sys.path.append('lib/')
from oracle_runner import OracleRunner

def main():
    runner_object   =   Runner()
    runner_object.test_connection()

def main_with_creds(db_user, db_password, sid):
    oracle_runner_obj   =   OracleRunner(db_user, db_password, sid)
    
    QUERY = u'SELECT 1 FROM DUAL'
    result = oracle_runner_obj.run(QUERY)
    
    if result['data'][0][0] == 1:
        print("Connection Test Succesful.")
        return True
        
    print("Connection Test Failed.")
    return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Database connection Tester.')
    parser.add_argument('-DB_USERNAME', help="Database Username")
    parser.add_argument('-DB_PASSWORD', help="Database Password")
    parser.add_argument('-SID', help="oracle system identifier")    
    
    args         =   parser.parse_args()
    db_user      =   args.DB_USERNAME
    db_password  =   args.DB_PASSWORD
    sid          =   args.SID
    
    if db_user and db_password and sid:
        
        if main_with_creds(db_user, db_password, sid):
            sys.exit(0)
        else:
            sys.exit(1)
        
    elif db_user or db_password or sid:
        
        print("All three parameters DB_USERNAME, DB_PASSWORD, SID required.")
        sys.exit(1)
    
    else:
        main()