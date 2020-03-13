#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "June 2018"

import os
from database import db_query
from utilities import md5Checksum
from datetime import datetime
from datetime import timedelta
from utilities import LoggingClass
from read_json import ReadJson
from database import MySQLDatabase
from utilities import SendEmail

rj = ReadJson()
log = LoggingClass('',True).get_logger()

class StorageFilesList(object):
    def __init__(self):
        self.months = int(rj.get_months())
        self.strg_fldr = rj.get_storage_folder()

    def create_storage_list(self):
        files_list = []
        for root,subdirs,files in os.walk(self.strg_fldr):
            for filename in files:
                file_path = os.path.join(root, filename)
                files_list.append(file_path) 
        return files_list

    def create_selected_list(self):
        limit_date = [(datetime.now() + timedelta(-30*(self.months))).strftime('%Y/%m/%d')]
        selected_list = []
        for i in StorageFilesList().create_storage_list():
            date_from_path = os.path.relpath(i, self.strg_fldr)[:10]
            if date_from_path < limit_date[0]:
                selected_list.append(i)
        return selected_list

def main():
    dbuser = rj.get_db_user();  dbpwd = rj.get_db_pwd()   
    dbhost = rj.get_db_host();  dbname = rj.get_db_name()   
    dbport = rj.get_db_port();  dbtables = rj.get_db_tables()
    sender = rj.get_sender();   smtphost = rj.get_smtp_host() 
    recipient = rj.get_recipient() 

    db = MySQLDatabase(dbuser, dbpwd, dbhost, dbport, dbname)

    Session = db.create_session()
    
    files_list = StorageFilesList().create_selected_list()

    for file_path in files_list:
        cksgz_stg = md5Checksum(file_path).calculate_checksum()
        cks_stg = md5Checksum(file_path).get_checksum_gz()
        head, fname_gz = os.path.split(file_path)

        for tbl in dbtables:
            db_element = db_query(tbl, Session, fname_gz) 

            if db_element is not None:
                cks_db = db_element[1]
                cksgz_db = db_element[2]
                if cks_db is not None and cksgz_db is not None:

                    if cksgz_stg == cksgz_db and cks_stg == cks_db:

                        try:
                             print(file_path)
                             #os.remove(file_path)
                        except Exception as e:
                            msg = "File removal exception --"
                            log.error("{0}{1}".format(msg,e))  	
   
                    else:
                        message = 'Severe alert - storage and DB file checksums DO NOT MATCH'
                        SendEmail(message,recipient,sender,smtphost).send_email()
    
                else:
                    message = 'Severe alert - checksum not calculated' 
                    SendEmail(message,recipient,sender,smtphost).send_email()
            else:
                pass

    db.close_session()

if __name__ == "__main__":
    main()
