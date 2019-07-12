#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "July 2019"

import os

def fileRemoval(i,sql,cur,full_fit,file):
        cur.execute(sql, [full_fit])
        if cur.rowcount == 1:
                try:
			file.write(i + '\n')
                        os.remove(i)
                except Exception as e:
                        e = sys.exc_info()
                        file.write(str(e[1]))
