#!/usr/bin/python
# -*- coding: utf8 -*-

from subprocess import Popen, PIPE
import random


def plat_form():
    ps = Popen("uname -a", shell=True, stdout=PIPE)
    ps.wait()

    output, errmsg = ps.communicate()

    if output.split(' ')[0] == "Linux":
        return "Linux"
    elif output.split(' ')[0] == "Darwin":
        return "Mac"
    else:
        return "Unknown"


def md5sum(file_name):
    plat = plat_form()

    if plat == "Unknown":
        return ""

    cmd = "md5 %s" if plat == "Mac" else "md5sum %s"

    get_result = (lambda x: x.split('=')[1].strip()) if plat == "Mac" else (lambda x: x.split(' ')[0].strip())

    sub_pro = Popen(cmd % file_name, shell=True, stdout=PIPE, stderr=PIPE)

    sub_pro.wait()

    result, errmsg = sub_pro.communicate()

    if errmsg:
        return ""

    md5 = get_result(result)

    return md5


# 随机生成手机号码
def createPhone():
    prelist = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152",
               "153", "155", "156", "157", "158", "159", "186", "187", "188"]
    return random.choice(prelist) + "".join(random.choice("0123456789") for i in range(8))
