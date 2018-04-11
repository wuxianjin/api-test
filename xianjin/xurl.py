#! /usr/bin/env python
# -*- coding:utf-8 -*-
""" 
@author:xianjin 
@file: xurl.py 
@time: 2018-04-11-19 
"""
from urllib import urlencode

params = urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})
print params
