# -*- coding: utf-8 -*-
"""
Created on Mon Dec 24 16:06:35 2018

@author: com-ftrojan
"""

from pydrive.auth import GoogleAuth

gauth = GoogleAuth()
gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.
#gauth.CommandLineAuth()
#TypeError: __init__() got an unexpected keyword argument 'openType'