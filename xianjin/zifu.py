#! /usr/bin/env python
# -*- coding:utf-8 -*-
""" 
@author:xianjin 
@file: zifu.py 
@time: 2018-04-08-16
"""
from conf import apiconf

schem = "https" if apiconf.API_PORT == 443 else "http"
host = apiconf.OPENBDP_HOST
port = apiconf.OPENBDP_PORT
url_host = "%s://%s:%s" % (schem, host, port)
print url_host
