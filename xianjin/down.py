#! /usr/bin/env python
# -*- coding:utf-8 -*-
""" 
@author:xianjin 
@file: down.py 
@time: 2018-03-05-14 
"""
import requests
import gzip
import os
import wget
import urllib2






def un_gz(file_name):
    f_name = file_name.replace(".gz", "")
    # 获取文件的名称，去掉
    g_file = gzip.GzipFile(file_name)
    # 创建gzip对象
    open(f_name, "w+").write(g_file.read())
    # gzip对象用read()打开后，写入open()建立的文件中。
    g_file.close()
    # 关闭gzip对象


def openbdp_tb_down():
    raw_resp = requests.get(
        'https://openapi.bdp.cn/v2/tb/export/download?task_id=task_55280bb88c214240bc1338631052f0e9&access_token=c3fc5154b650f80da08d5dbe60c6ca54')

    # raw_resp = requests.get(
    #     'https://www.bdp.cn/api/export/download?export_id=2362417228a73b852b983583076db73f&access_token=c3fc5154b650f80da08d5dbe60c6ca54')

    content_len = int(raw_resp.headers["Content-Length"])
    content_disp = raw_resp.headers["Content-Disposition"]
    content_dict = {}
    for i in content_disp.split(';'):
        try:
            k, v = i.split('=')
        except:
            k, v = "", ""

        if k:
            content_dict[k.strip()] = v.strip().strip('"')

    local_file = content_dict["filename"]
    fp = open("%s/%s" % (os.getcwd(), local_file), "wb")
    for i in raw_resp.iter_content(chunk_size=4096):
        fp.write(i)

    assert fp.tell() == content_len

    fp.close()
    os.rename(local_file, 'ttt.csv.gz')
    un_gz('ttt.csv.gz')


# openbdp_tb_down()
url = 'https://openapi.bdp.cn/v2/tb/export/download?task_id=task_55280bb88c214240bc1338631052f0e9&access_token=c3fc5154b650f80da08d5dbe60c6ca54'

# f = urllib2.urlopen(url)
# with open("code3.zip", "wb") as code:
#    code.write(f.read())

# r = requests.get(url, verify=False)
# print(r.content)
# with open("myCY2016.csv", "wb") as code:
#     code.write
#
#
#  r = requests.post(url)
# with open("demo4.csv.gz", "wb") as file:  # 文件名通过解析url地址得到
#    file.write(r.content)


# import csv
#
# with open('openbdptbdown.csv', 'rb') as f:
#     reader = csv.reader(f)
#     list = []
#     for row in reader:
#         list.append(row)
#
# assert len(list) == 6
# assert list[0] == ['date', 'name', 'value', 'key']
# assert list[5] == ['2012-12-30 00:00:00', 'A2', '2', 'key2']
