#! /usr/bin/env python
# -*- coding:utf-8 -*-
""" 
@author:xianjin 
@file: xjson.py 
@time: 2018-04-08-17 
"""
import json

name_emb = {'a':'1111','b':'2222','c':'3333','d':'4444'}
#传参
jsDumps = json.dumps(name_emb)
#获取返回值 用于将str类型的数据转成dict
# 'a'变成了u'a'是因为发生了类型转换，str会转换成unicode
jsLoads = json.loads(jsDumps)

print(name_emb)
print(type(name_emb))

print(jsDumps)
print(type(jsDumps))

print(jsLoads)
print(type(jsLoads))




# class B(object):
#     def ttt(self):
#         return "hell"
#
# a = B()
# method = getattr(a, "ttt")
#
# print str(method)
