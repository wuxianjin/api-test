#!/usr/bin/python
# -*- coding: utf8 -*-

import os
import json
import copy
from conf import bdpconf
from lib.BdpSDK import BdpSDK
import time
import random


def COUNT(field):
    nfield = copy.deepcopy(field)

    nfield["aggregator"] = "COUNT"

    return nfield


def SUM(field):
    nfield = copy.deepcopy(field)

    nfield["aggregator"] = "SUM"

    return nfield


def make_init(some_class):

    if some_class.inited:
        return some_class

    some_class.init()
    return some_class


@make_init
class bdp_tables:

    """

    """
    inited = False

    @classmethod
    def init(cls):

        if cls.inited:
            return

        meta_file = os.getcwd() + ("/data/cache/%s" % bdpconf.META_CACHE_FILE)

        cls.json_raw = ""
        cls.json_obj = dict()

        with open(meta_file) as fp:
            cls.json_raw = fp.read()
            cls.json_obj = json.loads(cls.json_raw)

        # 使用深拷贝副本，避免修改
        meta = copy.deepcopy(cls.json_obj)
        assert "tables" in meta and "charts" in meta

        cls.tables = meta["tables"]
        cls.charts = meta["charts"]
        cls.basic_projects = meta["basic_projects"]
        cls.inited = True

    @classmethod
    def table_from_name(cls, tb_name):
        return bdp_table(cls.tables[tb_name])

    @classmethod
    def global_basic_project(cls):
        return cls.basic_projects

    @classmethod
    def global_dshid(cls):

        if not getattr(cls, "dsh_id", ""):

            bdp = BdpSDK.instance()
            dsh_name = "dsh_1_%s_%s" % (time.time(), random.randint(0, 100000))

            bdp_basic_project_name = "%s%s" % (bdpconf.PROJECT_NAME, random.randint(0, bdpconf.PROJECT_NUM - 1))
            if bdp_basic_project_name in bdp_tables.global_basic_project():
                proj_id = bdp_tables.global_basic_project()[bdp_basic_project_name]

            else:
                proj_id = bdp.call_method_and_succ(
                    "project_create",
                    "proj_for_%s" % dsh_name,
                    ret_expr='["result"]["proj_id"]'
                )
            cls.proj_id = proj_id
            cls.dsh_id = bdp.call_method_and_succ("dsh_create", dsh_name, proj_id, ret_expr='["result"]["dsh_id"]')

        return cls.dsh_id

    def __init__(self):
        pass


class bdp_table:

    """

    """

    class BdpField(dict):

        _map = {
            2: "string",
            3: "date",
            1: "number",
        }

        _rmap = {
            "string": 2,
            "date": 3,
            "number": 1,
        }

        def as_subdate(self, sub_str):
            if self.type_str() != "date":
                assert False

            assert sub_str in ("year", "month", "day", "quarter", "week", "hour", "minute", "second")

            new_field = copy.deepcopy(self)
            new_field["fid"] = self["fid"] + "_" + sub_str
            new_field["f_type_s"] = "sub_date"

            return new_field

        def type_str(self):
            if "f_type_s" in self:
                return self["f_type_s"]

            assert self["f_type"] in self._map
            return self._map[self["f_type"]]

        def type_int(self):
            if "f_type" in self:
                return self["f_type"]

            assert self["f_type_s"] in self._rmap
            return self._rmap[self["f_type_s"]]

        def is_build_aggregated(self):
            if "is_build_aggregated" in self:
                return self.get("is_build_aggregated")

            return 0

    def __init__(self, tb_dict):
        self.meta = tb_dict

    def tb_id(self):
        return self.meta['tb_id']

    def tb_name(self):
        return self.meta["name"]

    def fields_list(self):
        return [self.BdpField(i) for i in self.meta["fields"]]

    def field_from_name(self, field_name):

        if not field_name:
            return None

        legal_subdate_list = ("year", "month", "day", "quarter", "week", "hour", "minute", "second")

        subdate = (False, "")
        # 子日期传入字段名称形如:字段名称 + "_as_month"
        for sub_str in legal_subdate_list:
            if field_name.endswith("_as_" + sub_str):
                subdate = (True, sub_str)

        if subdate[0]:
            fd_name = field_name[:-1*len("_as_" + subdate[1])]
        else:
            fd_name = field_name

        for fd in self.meta["fields"]:
            if fd["f_name"] == fd_name:
                _t = self.BdpField(fd)
                _t.tb_id = self.tb_id()

                if subdate[0]:
                    field = _t.as_subdate(subdate[1])
                else:
                    field = _t

                return field

    def field_from_resp(self, resp):
        fd = self.BdpField()
        fd["tb_id"] = self.tb_id()
        fd["f_type_s"] = resp["data_type"]
        fd["fid"] = resp["fid"]
        fd["f_name"] = resp["name"]
        fd["formula"] = resp["formula"]
        fd["param"] = resp["param"]
        fd["is_build_aggregated"] = resp["is_build_aggregated"]
        fd["type"] = resp["type"]
        return fd

try:
    bdp_tables.init_meta()
except:
    pass


