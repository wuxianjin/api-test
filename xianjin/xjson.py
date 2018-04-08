#! /usr/bin/env python
# -*- coding:utf-8 -*-
""" 
@author:xianjin 
@file: xjson.py 
@time: 2018-04-08-17 
"""
import json

data = [
    {
        "name": "密级",
        "type": "text",
        "config": {
            "hint": "Please input..."
        }
    },

    {
        "name": "手机品牌",
        "type": "select",
        "config": {
            "options": ["apple", "vivo", "huawei"]
        }
    }
]
print data
print "\r"
data = json.dumps(data)
print data
