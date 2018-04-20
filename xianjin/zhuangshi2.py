#! /usr/bin/env python
# -*- coding:utf-8 -*-
""" 
@author:xianjin 
@file: zhuangshi2.py 
@time: 2018-04-19-15 
"""

'''《1》万物皆对象'''
# def cal(x, y):
#     result = x + y
#     return result
#
#
# print cal(1,2)
# tt = cal
# print tt(1,2)



'''
进化一
'''

# def a():
#     pass
#
#
# def b():
#     pass
#
#
# def c():
#     pass
#
#
# def decorator(func):
#     print 'Start %s' % func.func_name
#     func()


# decorator(a)
# decorator(b)
# decorator(c)

'''
进化二 abc三个函数带参数怎么办  装饰器2
'''
'''decorator函数返回的是wrapper, wrapper是一个函数对象。而a = decorator(a)就相当于是把 a 指向了 wrapper,
 由于wrapper可以有参数，于是变量 a 也可以有参数了！'''
def decorator(func):
    def wrapper(*arg, **kw):
        print 'Start %s' % func.func_name
        return func(*arg, **kw)

    return wrapper


def a(arg):
    pass


def b(arg):
    pass


def c(arg):
    pass


# 将a = decorator(a)这个过程给自动化呢 @decorator
# a = decorator(a)
# b = decorator(b)
# c = decorator(c)
#
# a(1)
# b(1)
# c(1)

'''要是我的装饰器中也有参数该怎么办呢？再加一层就解决了。'''


def decorator2(arg_of_decorator):
    def log(func):
        def wrapper2(*arg, **kw):
            print 'Start %s' % func.func_name
            # TODO Add here sentences which use arg_of_decorator
            return func(*arg, **kw)

        return wrapper2
    return log
a = decorator2(a)
b = decorator2(b)
c = decorator2(c)

a(1)
b(1)
c(1)