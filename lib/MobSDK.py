#! /usr/bin/env python
# -*- coding:utf-8 -*-
""" 
@author:xianjin 
@file: MobSDK.py 
@time: 2018-04-17-14 
"""
import json
from urllib import urlencode
import time
import uuid
from random import randint
from lib.APIRequest import APIRequest
from conf import apiconf
from util import log


def dec_log(reserved_param=None):
    def _out_wrap(func):
        def _wrap_func(*args, **kwargs):
            rst = func(*args, **kwargs)
            assert isinstance(args[0], OpenbdpSdk)
            log.getlog(APIRequest.LOG_NAME).debug("API [%s] Response: %s" % (func.func_name, args[0].raw_data))
            return rst

        _wrap_func.__name__ = func.__name__
        return _wrap_func

    return _out_wrap


class OpenbdpSdk:
    _sdk_instance = None
    # open api user
    open_api_userInfo = '/user/info'
    open_api_tb_down = '/tb/export/download'
    # chart data
    open_api_chart_data = '/chart/data'



    def __init__(self, access_token="", version=""):
        self.raw_data = {}
        self.access_token = access_token
        self.version = version
        self.http_request = APIRequest(apiconf.OPENBDP_HOST, apiconf.OPENBDP_PORT)
        # online
        self.http_request.url_host = "%s/%s" % (self.http_request.url_host, self.version)
        # add headers
        self.http_request.add_header("Content-Type", "application/x-www-form-urlencoded;charset=UTF-8")
        self.trace_id = ""

    @classmethod
    def instance(cls):
        if not cls._sdk_instance:
            cls._sdk_instance = OpenbdpSdk(apiconf.OPENBDP_TOKEN, apiconf.OPENBDP_VERSION)

        return cls._sdk_instance

    def build_post_param(self, params):
        str_data = ""

        if isinstance(params, dict):
            str_data = urlencode(params)
        elif isinstance(params, list):
            str_data = "\r\n".join(params)
        elif isinstance(params, str):
            str_data = params
        else:
            assert 0

        return str_data

    def build_url(self, url, params=None):

        if params is None:
            params = {
                'access_token': self.access_token
            }

        else:
            assert isinstance(params, dict)

        self.trace_id = "trace_%s" % uuid.uuid3(uuid.NAMESPACE_DNS, "%s_%s_%s" % (url, time.time(), randint(0, 100000)))
        params["trace_id"] = self.trace_id
        return "%s?%s" % (url, urlencode(params))

    # todo
    def call_method_and_succ(self, method_name, *args, **kwargs):
        # 判断一个对象里面是否有name属性或者name方法，返回BOOL值
        if hasattr(self, method_name):
            # 获取对象的属性或者方法
            method = getattr(self, method_name)
            # 用于检查一个对象/方法是否是可调用
            if callable(method):
                method(*args)
                # json.loads()用于将str类型的数据转成dict
                resp = json.loads(self.raw_data)
                assert resp["status"] == "0"
                if "ret_expr" in kwargs:
                    # 把str转化为dict
                    return eval("resp" + kwargs['ret_expr'])
            else:
                log.getlog().debug("attribute[%s] not callable" % method_name)
        else:
            log.getlog().debug("function %s not found" % method_name)

    def _send_post(self, short_api, body={}):

        url = self.build_url(short_api)
        raw_body = self.build_post_param(body)

        self.raw_data = self.http_request.post(url, raw_body).read()





    @dec_log()
    def openbdp_chart_data(self, ct_id):
        req_param = {
            "ct_id": ct_id
        }
        self._send_post(self.open_api_chart_data, req_param)

