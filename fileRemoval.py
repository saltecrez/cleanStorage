#!/usr/bin/env python

__author__ = "Elisa Londero"
__email__ = "elisa.londero@inaf.it"
__date__ = "July 2019"

import os

def fileRemoval(i, sql, cur, full_fit, logfile):
        cur.execute(sql, [full_fit])
        if cur.rowcount == 1:
                try:
			logfile.write(i + '\n')
                        os.remove(i)
                except Exception as e:
                        e = sys.exc_info()
                        logfile.write(str(e[1]))
