#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "June 2018"

import os
#from glob import glob
##from database import db_query
#from utilities import md5Checksum
from datetime import datetime
from datetime import timedelta
from utilities import LoggingClass
from read_json import ReadJson
#from database import MySQLDatabase
#from utilities import MissingConfParameter
#from utilities import SendEmail

rj = ReadJson()
log = LoggingClass('',True).get_logger()

class StorageFilesList(object):
    def __init__(self):
        self.months = int(rj.get_months())
        self.strg_fldr = rj.get_storage_folder()

    def create_list(self):
        files_list = []
        for root,subdirs,files in os.walk(self.strg_fldr):
            for filename in files:
                file_path = os.path.join(root, filename)
                files_list.append(file_path) 
        return files_list

    def select_dates(self):
        date_in_past = [(datetime.now() + timedelta(-30*(self.months))).strftime('%Y/%m/%d')]
        selected_list = []
        for i in StorageFilesList().create_list():
            date_from_path = os.path.relpath(i, self.strg_fldr)[:10]
            if date_from_path < date_in_past[0]:
                selected_list.append(i)
        print(selected_list)
        return selected_list




def main():
    dbuser = rj.get_db_user();  dbpwd = rj.get_db_pwd()   
    dbhost = rj.get_db_host();  dbname = rj.get_db_name()   
    dbport = rj.get_db_port();  dbtables = rj.get_db_tables()
    sender = rj.get_sender();   smtphost = rj.get_smtp_host() 
    recipient = rj.get_recipient() 

    db = MySQLDatabase(dbuser, dbpwd, dbhost, dbport, dbname)

    Session = db.create_session()
    
    files_list = StorageFilesList().create_list()

    for file_path in files_list:
        cks_newdata = md5Checksum(file_path).calculate_checksum()
        fname = os.path.basename(os.path.splitext(os.path.normpath(file_path))[0])
        fname_gz = fname + '.fits.gz' 

        for tbl in dbtables:
            db_element = db_query(tbl, Session, fname_gz) 

            if db_element is not None:
                storage_path = db_element[0]
                cks_db = db_element[1]
                cksgz_db = db_element[2]
                cksgz_stg = md5Checksum(storage_path).calculate_checksum() 
                cks_stg = md5Checksum(storage_path).get_checksum_gz()
                if cksgz_stg == cksgz_db and cks_stg == cks_db == cks_newdata:
                    try:
                        os.remove(file_path)
                    except Exception as e:
                        msg = "File removal exception --"
                        log.error("{0}{1}".format(msg,e))  	
                else: 
                    message = 'Severe alert - newdata, storage and DB file checksums DO NOT MATCH'
                    SendEmail(message,recipient,sender,smtphost).send_email()
            else:
                pass

    db.close_session()

if __name__ == "__main__":
    #main()
    stor_path = '/home/archivio/tmp_storage/'
    StorageFilesList().select_dates()
