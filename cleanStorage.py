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
from readJson import readJson
from fileRemoval import fileRemoval

# Get current working directory
CWD = os.path.dirname(os.path.abspath(sys.argv[0]))

# Load input file 
cnf = readJson('config.json', CWD)

# Open logfile 
filelog = open(CWD + '/' + cnf['logfile'], 'a')

# create files list
walk_dir = cnf['storage_folder']

# connect to DB
db = MySQLdb.connect(cnf['remote_db_host'], cnf['remote_db_user'], cnf['remote_db_password'], cnf['remote_db_schema'])
cur = db.cursor()

# instruments list
instr_list = cnf['file_init'] 
sql_list = cnf['sql_instr'] 

for root, subdirs, files in os.walk(walk_dir):

	for filename in files:

		file_path = os.path.join(root, filename)
		ftl = filename[:2]

		for j in range(len(instr_list)):
			if ftl == instr_list[j]:
				sql = 'select id from ' + sql_list[j] + ' where file_name=%s;' 
				fileRemoval(file_path, sql, cur, filename, filelog)
				break
			else:
				continue

filelog.close()
