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


def dec_log(func):
    def _wrap_func(*args, **kwargs):
        func(*args, **kwargs)
        assert isinstance(args[0], mobSdk)
        log.getlog(APIRequest.LOG_NAME).debug("API [%s] Response: %s" % (func.func_name, args[0].raw_data))

    return _wrap_func


class mobSdk:
    _sdk_instance = None
    mob_chartdata = '/mob/chart/data'

    def __init__(self, access_token=""):
        self.raw_data = {}
        self.access_token = access_token
        self.http_request = APIRequest(apiconf.API_HOST, apiconf.API_PORT)
        self.http_request.url_host = "%s" % (self.http_request.url_host)
        self.http_request.add_header("Content-Type", "application/x-www-form-urlencoded;charset=UTF-8")
        self.trace_id = ""

    @classmethod
    def instance(cls):
        if not cls._sdk_instance:
            cls._sdk_instance = mobSdk(apiconf.MOB_TOKEN)

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
        # params["system"] = 'android'
        return "%s?%s" % (url, urlencode(params))

    # todo
    def call_method_and_succ(self, method_name, *args, **kwargs):
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            if callable(method):
                method(*args)
                resp = json.loads(self.raw_data)
                assert resp["status"] == "0"
                if "ret_expr" in kwargs:
                    return eval("resp" + kwargs['ret_expr'])
            else:
                log.getlog().debug("attribute[%s] not callable" % method_name)
        else:
            log.getlog().debug("function %s not found" % method_name)

    def _send_post(self, short_api, body={}):

        url = self.build_url(short_api)
        raw_body = self.build_post_param(body)

        self.raw_data = self.http_request.post(url, raw_body).read()

    @dec_log
    def mob_chart_data(self, system, app_ver, ct_id):
        req_param = {
            "ct_id": ct_id,
            "system": system,
            "app_ver": app_ver

        }
        self._send_post(self.mob_chartdata, req_param)
