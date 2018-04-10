#! /usr/bin/env python
# -*- coding:utf-8 -*-
""" 
@author:xianjin 
@file: args.py 
@time: 2018-04-10-17 
"""
'''
声明一个诸如 * param
的星号参数时，从此处开始直到结束的所有位置参数 （Positional
Arguments）都将被收集并汇集成一个称为“param”的元组（Tuple）。 类似地，当我们声明一个诸如 ** param
的双星号参数时，从此处开始直至结束的所有关键字
参数都将被收集并汇集成一个名为
param的字典（Dictionary）。'''

def argsFunc(a, *args):
    print a
    print args


argsFunc(1, "tt", 3)
# ('tt', 3)
'''
形参名前加两个*表示，参数在函数内部将被存放在以形式名为标识符的 dictionary 中，这时调用函数的方法则需要采用 arg1=value1,arg2=value2 这样的形式。

为了区分，我把 *args 称作为数组参数，**kwargs 称作为字典参数
'''
def kwargsFunc(a,**kwargs):
    print a
    print kwargs


kwargsFunc(1,name='wxj',psword="123")

# 合用时*args必须位于**kwargs之前
def test_kwargs(first, *args, **kwargs):
   print 'Required argument: ', first
   print kwargs
   for v in args:
      print 'Optional argument (*args): ', v
   for k, v in kwargs.items():
      print 'Optional argument %s (*kwargs): %s' % (k, v)


test_kwargs(1, 2, 3, 4, k1=5, k2=6)
