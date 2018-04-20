#!/usr/bin/python
# -*- coding: utf8 -*-

import logging
import os
from conf import apiconf
import time


log_dict = {}

if not os.path.exists(apiconf.LOG_DIR):
    os.mkdir(apiconf.LOG_DIR)


def getlog(name="api_auto"):

    if name in log_dict:
        return log_dict[name]
    # 初始化logger后面的日志格式中的 % (name)s对应的是这里的模块名字
    logger = logging.getLogger(name)
    # 设置级别 有NOTSET < DEBUG < INFO < WARNING < ERROR < CRITICAL这几种级别，日志会记录设置级别以上的日志
    logger.setLevel(logging.DEBUG)
    # Handler，常用的是StreamHandler和FileHandler一个打印在CMD窗口上，一个记录在一个文件上
    hd = logging.FileHandler(filename="%s/%s.log.%s" % (apiconf.LOG_DIR, name, time.strftime("%F", time.localtime(time.time()))))
    # 常用日志格式，
    formatter = logging.Formatter("%(asctime)s - %(funcName)s - %(levelname)s - %(message)s")
    hd.setFormatter(formatter)
    logger.addHandler(hd)
    log_dict[name] = logger
    return logger


'''
formatter，
%(asctime)s 字符串形式的当前时间。默认格式是 “2003-07-08 16:49:45,896”。逗号后面的是毫秒
%(funcName)s 调用日志输出函数的函数名
%(levelname)s 文本形式的日志级别
%(message)s 用户输出的消息

%(name)s Logger的名字
%(levelno)s 数字形式的日志级别
%(pathname)s 调用日志输出函数的模块的完整路径名，可能没有
%(filename)s 调用日志输出函数的模块的文件名
%(module)s  调用日志输出函数的模块名
%(lineno)d 调用日志输出函数的语句所在的代码行
%(created)f 当前时间，用UNIX标准的表示时间的浮 点数表示
%(relativeCreated)d 输出日志信息时的，自Logger创建以 来的毫秒数
%(thread)d 线程ID。可能没有
%(threadName)s 线程名。可能没有
%(process)d 进程ID。可能没有
'''