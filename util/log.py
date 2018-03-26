#!/usr/bin/python
# -*- coding: utf8 -*-

import logging
import os
from conf import apiconf
import time


log_dict = {}

if not os.path.exists(apiconf.LOG_DIR):
    os.mkdir(apiconf.LOG_DIR)


def getlog(name="bdp_auto"):

    if name in log_dict:
        return log_dict[name]

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    hd = logging.FileHandler(filename="%s/%s.log.%s" % (apiconf.LOG_DIR, name, time.strftime("%F", time.localtime(time.time()))))
    formatter = logging.Formatter("%(asctime)s - %(funcName)s - %(levelname)s - %(message)s")
    hd.setFormatter(formatter)
    logger.addHandler(hd)
    log_dict[name] = logger
    return logger
