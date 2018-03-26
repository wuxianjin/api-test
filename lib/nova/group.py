#!/usr/bin/python
# -*- coding: utf8 -*-
# __author__ = '5xianjin'
from lib.BdpSDK import BdpSDK
from lib.openbdp_sdk import OpenbdpSdk
import json
import pytest


# 此后扩展为分组结构
class group(object):
    def __init__(self):
        self.bdp = BdpSDK.instance()
        self.name = ""
        self.g_id = ""
        self.p_id = ""

    def name(self):
        return self.name

    def id(self):
        return self.g_id

    def pid(self):
        return self.pid

    @classmethod
    def create(cls, name, pid):
        id = BdpSDK.instance().call_method_and_succ("groupcreate", name, pid, ret_expr='["result"]')
        return id

    @classmethod
    def groupmodify(cls, gid,name=name,parent_group_id=pid):
        BdpSDK.instance().call_method_and_succ("groupmodify", gid, name=name, parent_group_id=parent_group_id,ret_expr='["result"]')

    @classmethod
    def grouplist(cls):
        return BdpSDK.instance().call_method_and_succ("grouplist", ret_expr='["result"]')

    @classmethod
    def groupinfo(cls, gid):
        return BdpSDK.instance().call_method_and_succ("groupinfo", gid, ret_expr='["result"]')

    @classmethod
    def groupdel(cls, gid):
        openbdp = OpenbdpSdk.instance()
        openbdp.call_method_and_succ("openbdp_groupdel", gid)
        with pytest.raises(AssertionError):
            cls.groupinfo(gid)
        assert json.loads(BdpSDK.instance().raw_data)["status"] == "4"
