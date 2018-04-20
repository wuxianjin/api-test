#! /usr/bin/env python
# -*- coding:utf-8 -*-
""" 
@author:xianjin 
@file: zhuangshiqi.py 
@time: 2018-04-18-15
https://www.zhihu.com/question/26930016
"""
from util import log
from lib.APIRequest import APIRequest


def use_log(func):
    def wrapper(*args, **kwargs):
        log.getlog(APIRequest.LOG_NAME).debug("%s is runing" % func.__name__)
        return func(*args, **kwargs)

    return wrapper


@use_log
def foo():
    print "i m foo"


@use_log
def bar():
    print "i m bar"



def bar2(x,y):
    print "i m ba2r"
    return x+y


# bar2()

tt = bar2
print tt(1,2)
