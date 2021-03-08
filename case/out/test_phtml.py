#! /usr/bin/env python
# -*- coding:utf-8 -*-
""" 
@author:xianjin 
@file: phtml.py 
@time: 2018-05-30-16 
"""
import pytest


# content of test_class.py
class TestClass:
    def test_one(self):
        print('one')
        x = "this"
        assert 'h' in x

    def test_two(self):
        print('two')
        x = "hello"
        assert hasattr(x, 'check')


if __name__ == '__main__':
    pytest.main("-q -vv --html=testreport.html")
