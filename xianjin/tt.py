#! /usr/bin/env python
# -*- coding:utf-8 -*-
""" 
@author:xianjin 
@file: tt.py 
@time: 2018-03-29-11 
"""
import time

# print time.localtime()
#
# print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
# print type(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

last_request_time = int(time.mktime(time.strptime(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), '%Y-%m-%d %H:%M:%S')))
print last_request_time

