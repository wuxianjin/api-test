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

# last_request_time = int(time.mktime(time.strptime(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), '%Y-%m-%d %H:%M:%S')))
# print last_request_time

# t = None
# print not None

name_emb = "{'a':'1111','b':'2222','c':'3333','d':'4444'}"
# 可以把list,tuple,dict和string相互转化
# print(eval(name_emb))
dd = {u'status': u'0', u'errstr': u'', u'result': [{u'type': u'text', u'config': {u'hint': u'Please input...'}, u'name': u'\u5bc6\u7ea7', u'id': u'field_1'}, {u'type': u'select', u'config': {u'options': [u'apple', u'vivo', u'huawei']}, u'name': u'\u624b\u673a\u54c1\u724c', u'id': u'field_2'}], u'request_id': u'ironman_2f586f01-d977-3a2b-95c0-5bdbfa0abf69'}

print(type(dd['result']))

