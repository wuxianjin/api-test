#! /usr/bin/env python
# -*- coding:utf-8 -*-
""" 
@author:xianjin 
@file: apiconf.py 
@time: 2018-03-26-15 
"""
# host
BDP_HOST = '5xianjin.bdpdev.bdp.cn'
BDP_PORT = 80

# timeout
TIME_OUT = 600
RETRY_TIMES = 3

REQUEST_TIMEOUT = 180

# log
LOG_DIR = "/tmp/logs/"

DOWNLOAD_DIR = "/tmp/"

# user bdp_autotest

BDP_USER = "admin"
BDP_PASS = "123qweasd"
BDP_DOMAIN = "ysn"

# for openbdp bdp_autotest
OPENBDP_HOST = '123.126.105.32'
OPENBDP_PORT = 15890
OPENBDP_TOKEN = '8e9548ad8e7645a3a40560828c488366'
OPENBDP_VERSION = 'v2'
#
# OPENBDP_HOST = 'openapi.bdp.cn'
# OPENBDP_PORT = 443
# # admin opends_token
# OPENBDP_TOKEN = 'ba7b265d40d0cc29f0a115b0ed350d81'
# OPENBDP_VERSION = 'v2'

# paralize
PROCESS_COUNT = 20
WAIT_TIME_OUT = 800

# prepare project
PROJECT_NAME = "BDP_BASIC_PROJECT"
PROJECT_NUM = 10
