#!/usr/bin/python
# -*- coding: utf8 -*-

import json
from urllib import urlencode
import time
import uuid
from random import randint
import requests
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
    open_api_userCreate = '/user/create'
    open_api_usermodify = '/user/modify'
    open_api_ufunmodify = '/user/func_modify'
    open_api_userdelete = '/user/delete'
    open_api_userlist = '/user/list'
    open_api_userfreeze = '/user/freeze'
    open_api_userunfreeze = '/user/unfreeze'
    open_api_reset_password = '/user/reset_password'
    open_api_bulk_delete = '/user/bulk_delete'
    # group
    open_api_group_list = '/group/list'
    open_api_group_create = '/group/create'
    open_api_group_info = '/group/info'
    open_api_group_delete = '/group/delete'
    open_api_group_modify = '/group/modify'
    open_api_group_adduser = '/group/add_user'
    open_api_group_deluser = '/group/del_user'
    open_api_group_addmanager = '/group/add_manager'
    open_api_group_delmanager = '/group/del_manager'
    open_api_group_update_fields = '/group/update_fields'
    open_api_group_list_fields = '/group/list_fields'
    # work table
    open_api_tb_share = '/tb/add_share'

    open_api_tb_export = '/tb/export/tb_file'
    open_api_tb_status = '/tb/export/status'
    open_api_tb_down = '/tb/export/download'
    # chart data
    open_api_chart_data = '/chart/data'

    def __init__(self, access_token="", version=""):
        self.raw_data = {}
        self.access_token = access_token
        self.version = version
        self.http_request = APIRequest(apiconf.OPENBDP_HOST, apiconf.OPENBDP_PORT)
        # offline
        # self.http_request.url_host = "%s/%s%s" % (self.http_request.url_host, 'api/', self.version)
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
            """
            for k, v in params.items():
                str_data += "%s=%s&" % (k, v)
            str_data = str_data.strip('&')
            """

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

        # if "access_token" not in body:
        #     body["access_token"] = self.access_token

        url = self.build_url(short_api)
        raw_body = self.build_post_param(body)

        self.raw_data = self.http_request.post(url, raw_body).read()

    def _json_post(self, short_api, params, body):

        assert isinstance(params, dict)

        if "access_token" not in params:
            params["access_token"] = self.access_token
        url = self.build_url(short_api, params)

        if type(body) is not str:

            self.raw_data = self.http_request.post(url, json.dumps(body)).read()
        else:
            self.raw_data = self.http_request.post(url, body).read()

    @dec_log()
    def openbdp_chart_data(self, ct_id):
        req_param = {
            "ct_id": ct_id
        }
        self._send_post(self.open_api_chart_data, req_param)

    @dec_log()
    def openbdp_group_list_fields(self):
        req_param = {

        }
        self._send_post(self.open_api_group_list_fields, req_param)

    @dec_log()
    def openbdp_group_update_fields(self, data):
        assert isinstance(data, list or json)
        # 用于将dict类型的数据转成str
        data = json.dumps(data)
        req_param = {
            "group_fields": data
        }
        self._send_post(self.open_api_group_update_fields, req_param)

    @dec_log()
    def openbdp_tb_share(self, group_id, data):
        assert isinstance(data, list or json)
        if isinstance(data, list or json):
            data = json.dumps(data)
        req_param = {
            "group_id": group_id,
            "user_ids": data
        }
        self._send_post(self.openbdp_tb_share, req_param)

    @dec_log()
    def openbdp_group_delmanager(self, group_id, data):
        assert isinstance(data, list or json)
        if isinstance(data, list or json):
            data = json.dumps(data)
        req_param = {
            "group_id": group_id,
            "user_ids": data
        }
        self._send_post(self.open_api_group_delmanager, req_param)

    @dec_log()
    def openbdp_group_addmanager(self, group_id, data):
        assert isinstance(data, list or json)
        if isinstance(data, list or json):
            data = json.dumps(data)
        req_param = {
            "group_id": group_id,
            "user_ids": data
        }
        self._send_post(self.open_api_group_addmanager, req_param)

    @dec_log()
    def openbdp_group_adduser(self, group_id, data):
        assert isinstance(data, list or json)
        if isinstance(data, list or json):
            data = json.dumps(data)
        req_param = {
            "group_id": group_id,
            "user_ids": data
        }
        self._send_post(self.open_api_group_adduser, req_param)

    @dec_log()
    def openbdp_group_deluser(self, group_id, data):
        assert isinstance(data, list or json)
        if isinstance(data, list or json):
            data = json.dumps(data)
        req_param = {
            "group_id": group_id,
            "user_ids": data
        }
        self._send_post(self.open_api_group_deluser, req_param)

    @dec_log()
    def openbdp_groupcreate(self, name, parent_id):
        req_param = {
            "name": name,
            "parent_id": parent_id

        }
        self._send_post(self.open_api_group_create, req_param)

    @dec_log()
    def openbdp_groupmodify(self, group_id, name, parent_id):
        req_param = {
            "group_id": group_id,
            "name": name,
            "parent_id": parent_id

        }
        self._send_post(self.open_api_group_modify, req_param)

    @dec_log()
    def openbdp_groupdel(self, group_id):
        req_param = {
            "group_id": group_id

        }
        self._send_post(self.open_api_group_delete, req_param)

    @dec_log()
    def openbdp_groupinfo(self, group_id):
        req_param = {
            "group_id": group_id

        }
        self._send_post(self.open_api_group_info, req_param)

    @dec_log()
    def openbdp_grouplist(self):
        req_param = {

        }
        self._send_post(self.open_api_group_list, req_param)

    @dec_log()
    def openbdp_reset_password(self, user_id):
        req_param = {
            "user_id": user_id
        }
        self._send_post(self.open_api_reset_password, req_param)

    @dec_log()
    def openbdp_userInfo(self, user_id):
        req_param = {
            # "access_token": access_token,
            "user_id": user_id
        }

        self._send_post(self.open_api_userInfo, req_param)

    @dec_log()
    def openbdp_userCreate(self, username, name, mobile, password, role, **kwargs):
        req_param = {
            "username": username,
            "name": name,
            "mobile": mobile,
            "password": password,
            "role": role,
        }
        for k, v in kwargs.iteritems():
            if not (isinstance(v, str) or isinstance(v, unicode)):
                kwargs[k] = json.dumps(v)
        req_param.update(kwargs)
        self._send_post(self.open_api_userCreate, req_param)

    @dec_log()
    def openbdp_user_bullkdel(self, data):
        assert isinstance(data, list or json)
        if isinstance(data, list or json):
            data = json.dumps(data)
        req_param = {

            "user_ids": data
        }
        self._send_post(self.open_api_bulk_delete, req_param)

    @dec_log()
    def openbdp_userfreeze(self, user_id):
        req_param = {
            "user_id": user_id
        }
        self._send_post(self.open_api_userfreeze, req_param)

    @dec_log()
    def openbdp_userunfreeze(self, user_id):
        req_param = {
            "user_id": user_id
        }
        self._send_post(self.open_api_userunfreeze, req_param)

    @dec_log()
    def openbdp_userlist(self, offset, limit):
        req_param = {
            "offset": offset,
            "limit": limit,
        }
        self._send_post(self.open_api_userlist, req_param)

    @dec_log()
    def openbdp_userdelete(self, user_id):
        req_param = {
            "user_id": user_id
        }
        self._send_post(self.open_api_userdelete, req_param)

    @dec_log()
    def openbdp_userdmodify(self, user_id, **kwargs):
        req_param = {
            "user_id": user_id
        }
        for k, v in kwargs.iteritems():
            if not (isinstance(v, str) or isinstance(v, unicode)):
                kwargs[k] = json.dumps(v)
        req_param.update(kwargs)
        self._send_post(self.open_api_usermodify, req_param)

    @dec_log()
    def openbdp_ufunmodify(self, user_id, **kwargs):
        req_param = {
            "user_id": user_id
        }
        for k, v in kwargs.iteritems():
            if not (isinstance(v, str) or isinstance(v, unicode)):
                kwargs[k] = json.dumps(v)
        req_param.update(kwargs)
        self._send_post(self.open_api_ufunmodify, req_param)

    @dec_log()
    def openbdp_tb_export(self, tb_id):
        req_param = {
            "tb_id": tb_id
        }
        self._send_post(self.open_api_tb_export, req_param)

    @dec_log()
    def openbdp_tb_status(self, task_id):
        req_param = {
            "task_id": task_id
        }
        self._send_post(self.open_api_tb_status, req_param)

    @dec_log()
    def openbdp_tb_down(self, task_id):
        req_param = {"task_id": task_id,
                     "access_token": apiconf.OPENBDP_TOKEN
                     }
        r = requests.get(self.http_request.url_host + self.open_api_tb_down, params=req_param)
        return r
