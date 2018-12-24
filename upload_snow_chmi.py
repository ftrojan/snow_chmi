# -*- coding: utf-8 -*-
"""
Created on Mon Dec 24 16:00:36 2018
Did not even try because the qdrive_quickstart.py authentication failed.
@author: com-ftrojan
"""
import os
import datetime


wdir = "data/%s" % datetime.datetime.today().strftime('%Y-%m-%d')
for fname in os.listdir(wdir):
    print(fname)