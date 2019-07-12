#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "July 2019"

'''
   This script is supposed to be used for the daily 
   cleaning of the LBT storage on *TEST MACHINES*
'''

import sys
import os
import MySQLdb
from shutil import Error
from readJson import readJson
from fileRemoval import fileRemoval

# Get current working directory
CWD = os.path.dirname(os.path.abspath(sys.argv[0]))

# Load input file 
cnf = readJson('config.json',CWD)

# Open logfile 
filelog = open(CWD + '/' + cnf['logfile'],'a')

# create files list
walk_dir = cnf['storage_folder']

# connect to DB
db = MySQLdb.connect(cnf['remote_db_host'],cnf['remote_db_user'],cnf['remote_db_password'],cnf['remote_db_schema'])
cur = db.cursor()

for root, subdirs, files in os.walk(walk_dir):

	for filename in files:

		file_path = os.path.join(root, filename)
		ftl = filename[:3]

		if ftl == 'luc':
			sql = cnf['sql_luci']
			fileRemoval(file_path,sql,cur,filename,filelog)

		elif ftl == 'mod':
        	        sql = cnf['sql_mods']
			fileRemoval(file_path,sql,cur,filename,filelog)

		elif ftl == 'lbc':
        	        sql = cnf['sql_lbc']
			fileRemoval(file_path,sql,cur,filename,filelog)

filelog.close()
