#!/usr/bin/python
# -*- coding: utf8 -*-
# __author__ = '5xianjin'
from lib.BdpSDK import BdpSDK
from conf import apiconf
import random
from lib.openbdp_sdk import OpenbdpSdk
import json
import pytest
from util import util
import  time


# 此后扩展为账号部分的自动化
class Account(object):
    def __init__(self):
        self.user_name = ""
        self.user_id = ""
        self.email = ""
        self.phone = ""
        self.bdp = BdpSDK.instance()

    def name(self):
        return self.user_name

    def id(self):
        return self.user_id

    def email(self):
        return self.email

    def phone(self):
        return self.phone

    def getUid(self, username=apiconf.USER_NAME, password=apiconf.PASS_WORD):
        BdpSDK.instance().change_user(apiconf.BDP_DOMAIN, username, password)
        uid = BdpSDK.instance().call_method_and_succ("userinfo", ret_expr='["result"]["user_id"]')
        self.user_id = uid
        return uid

    @classmethod
    def create(cls, username, password, gid, admin=False):
        # 配置普通用户信息
        if admin:
            role = 2
            join_group_id_list = []
            # todo
            manage_group_id_list = [gid]
        else:
            role = 3
            manage_group_id_list = []
            # todo
            join_group_id_list = [gid]

        #"mobile": util.createPhone(),
        userinfo = {"domain": apiconf.BDP_DOMAIN, "username": username, "name": "name","mobile": util.createPhone(),
                    "email": "youxiang" + str(int(time.time())) + "@hotmail.com", "role": role, "sex": u"男", "position": "QAtest",
                    "manage_group_id_list": manage_group_id_list,
                    "join_group_id_list": join_group_id_list}
        uid = BdpSDK.instance().call_method_and_succ("usercreate", userinfo, ret_expr='["result"]')
        # 激活用户
        # BdpSDK.instance().call_method_and_succ("userinit", uid, password, ret_expr='["result"]')
        Account.init_pwd(uid,password)
        return uid

    @classmethod
    def init_pwd(cls, uid,password):
        BdpSDK.instance().call_method_and_succ("userinit", uid, password, ret_expr='["result"]')

    @classmethod
    def reset_pwd(cls, uid):
        BdpSDK.instance().call_method_and_succ("user_reset_pwd", uid, ret_expr='["result"]')

    @classmethod
    def subinfo(cls, sub_id):
        result = BdpSDK.instance().call_method_and_succ("subinfo", sub_id, ret_expr='["result"]')
        return result

    @classmethod
    def userfrozen(cls, sub_id_list, userfrozen):
        if not isinstance(sub_id_list, list):
            sub_id_list = [sub_id_list]
        sta = BdpSDK.instance().call_method_and_succ("userfrozen", sub_id_list, userfrozen, ret_expr='')
        return sta

    @classmethod
    def user_del(cls, sub_id):
        openbdp = OpenbdpSdk.instance()
        openbdp.call_method_and_succ("openbdp_userdelete", sub_id)
        with pytest.raises(AssertionError):
            cls.subinfo(sub_id)
        assert json.loads(BdpSDK.instance().raw_data)["status"] == "1009"

    @classmethod
    def user_login(cls, username, password):
        return BdpSDK.instance().call_method_and_succ("login", username, password, apiconf.BDP_DOMAIN, ret_expr='')
