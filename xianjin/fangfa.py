#! /usr/bin/env python
# -*- coding:utf-8 -*-
""" 
@author:xianjin 
@file: fangfa.py 
@time: 2018-04-12-15 
"""
import json
from util import log


class FF(object):
    def addf(self, a):
        print "ttttt"
        return "hello"+a

    def call_method(self, name, *args):
        # 判断一个对象里面是否有name属性或者name方法，返回BOOL值
        if hasattr(self, name):
            # 获取对象的属性或者方法
            method = getattr(self, name)
            # 用于检查一个对象/方法是否是可调用
            if callable(method):
                method(*args)
            else:
                print 'not call'
        else:
            print 'not found'


FF().call_method('addf', '1')

