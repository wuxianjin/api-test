#! /usr/bin/env python
# -*- coding:utf-8 -*-
""" 
@author:xianjin 
@file: apiconf.py 
@time: 2018-03-26-15 
"""
# host
# API_HOST = 'bdp.cn'
# API_PORT = 443
# host
API_HOST = '5xianjin.bdpdev.bdp.cn'
API_PORT = 80
# timeout
TIME_OUT = 600
RETRY_TIMES = 3
BDP_SMALL_EMULATE = False
REQUEST_TIMEOUT = 180

# log
LOG_DIR = "/tmp/logs/"

DOWNLOAD_DIR = "/tmp/"

# user bdp_autotest

USER_NAME = "admin"
PASS_WORD = "123qweasd"
BDP_DOMAIN = "ios"

# for openbdp bdp_autotest
# OPENBDP_HOST = '123.126.105.32'
# OPENBDP_PORT = 15890
# OPENBDP_TOKEN = '8e9548ad8e7645a3a40560828c488366'
# OPENBDP_VERSION = 'v2'
#
OPENBDP_HOST = 'openapi.bdp.cn'
OPENBDP_PORT = 443
# admin opends_token
OPENBDP_TOKEN = '6a6280e8489697d1a8d54c611815bd28'
OPENBDP_VERSION = 'v2'



MOB_TOKEN = 'e3feb1fc166f4856599b3a1e255b4bd92f77938e6ae393dd'
# paralize
PROCESS_COUNT = 20
WAIT_TIME_OUT = 800

# prepare project
PROJECT_NAME = "BDP_BASIC_PROJECT"
PROJECT_NUM = 10
