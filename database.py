#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "September 2019"

import os
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utilities import LoggingClass
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Table
from sqlalchemy import MetaData
from sqlalchemy.orm import mapper

log = LoggingClass('',True).get_logger()

class MySQLDatabase(object):
    def __init__(self, user, pwd, host, port, dbname):
        self.user = user
        self.pwd = pwd
        self.host = host
        self.port = port
        self.dbname = dbname

    def create_session(self):
        sdb = 'mysql+pymysql://%s:%s@%s:%s/%s'%(self.user,self.pwd,self.host,self.port,self.dbname)
        try:
            engine = create_engine(sdb)
            db_session = sessionmaker(bind=engine)
            return db_session()
        except Exception as e:
            msg = "Database session creation excep - MySQLDatabase.create_session -- "
            log.error("{0}{1}".format(msg,e))

    def validate_session(self):
        try:
            connection = self.create_session().connection()
            return True
        except Exception as e:
            msg = "Database session validation excep - MySQLDatabase.validate_session -- "
            log.error("{0}{1}".format(msg,e))
            return False

    def close_session(self):
        try:
            self.create_session().close()
            return True
        except Exception as e: 
            msg = "Database session closing excep - MySQLDatabase.close_session -- "
            log.error("{0}{1}".format(msg,e))
            return False

def db_query(tab, session, fname):
    metadata = MetaData()
    table_name = tab
    table_object = Table(table_name, metadata,
        Column('id', Integer, primary_key=True),
        Column('file_name', String(255)),
        Column('storage_path', String(255)),
        Column('file_path', String(255)),
        Column('file_version', Integer()),
        Column('checksum', String(255)),
        Column('checksum_gz', String(255)))

    class TableObject(object):
         pass

    try:
        mapper(TableObject, table_object)
        rows = session.query(TableObject)
        flt = rows.filter(TableObject.file_name == fname)
        for j in flt:
            if j.file_name:
                path = j.storage_path + j.file_path
                full_path = os.path.join(path,str(j.file_version),j.file_name)
                return full_path, j.checksum, j.checksum_gz
    except Exception as e:
        msg = "Database query excep - db_query -- "
        log.error("{0}{1}".format(msg,e))
