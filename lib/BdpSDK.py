#!/usr/bin/python
# -*- coding: utf8 -*-

import requests
from urllib import urlencode, unquote
import uuid
from lib.BdpRequest import BDPRequest
import random
from random import randint
import time
import os
import traceback
import json
import datetime
import math
import csv
import pdb
import copy
import pytest

from conf import bdpconf
from lib import log


# used to print log


def dec_log(reserved_param=None):
    def _out_wrap(func):
        def _wrap_func(*args, **kwargs):
            rst = func(*args, **kwargs)
            assert isinstance(args[0], BdpSDK)
            log.getlog(BDPRequest.LOG_NAME).debug("API [%s] Response: %s" % (func.func_name, args[0].raw_data))
            return rst

        _wrap_func.__name__ = func.__name__
        return _wrap_func

    return _out_wrap


def loop_succ(func):
    def _wrap_func(*args, **kwargs):
        rst = func(*args, **kwargs)
        ts = bdpconf.TIME_OUT
        while not rst and ts > 0:
            rst = func(*args, **kwargs)
            time.sleep(1)
            ts -= 1
        return rst

    return _wrap_func


def expect_succ(func):
    def _wrap(the_self, *args, **kwargs):
        func(the_self, *args, **kwargs)

        resp = json.loads(the_self.raw_data)

        assert str(resp["status"]) == '0'

        if 'result' in resp or u'result' in resp:
            assert str(resp["result"]) != 'failed'

    return _wrap


class BdpSDK:
    api_login = '/api/user/login'
    api_userinfo = '/api/user/info'
    # accounts
    api_subinfo = '/api/sub/info'
    api_userfrozen = '/api/user/set_frozen'
    api_usercreate = '/api/sub/create'
    api_userinit = '/api/user/init_pwd'
    api_userdel = '/api/sub/delete'
    api_userreset_pwd = '/api/user/reset_pwd'
    api_usermodify = '/api/sub/modify'
    api_funcmodify = '/api/sub/func_modify'
    api_groupcreate = '/api/group/create'
    api_grouplist = '/api/group/list'
    api_groupinfo = '/api/group/info'
    api_groupdel = '/api/group/del'
    api_groupmodify = '/api/group/modify'

    api_excelupload = '/api/excel/upload'
    api_excelexport = '/api/chart/export_excel'
    api_taskstatus = '/api/task/status'
    api_excelcreate = '/api/excel/create'
    api_excelpreview = '/api/excel/preview'
    api_excelparser = '/api/excel/parser'
    api_excelschema = '/api/tb/schema'
    api_tbmodify = '/api/tb/modify'
    api_tbpreview = '/api/tb/preview'
    api_tbdelete = '/api/tb/delete'
    api_tbbatchdelete = '/api/tb/delete_batch'
    api_tbstatus = '/api/tb/status'
    api_modelstruct = '/api/tb/model_struct'
    api_checkfielddepend = '/api/tb/check_field_dependency'
    api_tbcapacity = '/api/tb/list_info'
    api_tbstatgroup = '/api/tb/stat_group'
    api_tbcheckrely = '/api/tb/list_check_rely'

    api_excellist = '/api/excel/list'
    api_exceldelete = '/api/excel/delete'
    api_exceldownload = '/api/excel/download'
    api_getfiletype = '/api/export/get_file_type'
    api_exportlargefile = '/api/export/large_file'
    api_exportfilelist = '/api/export/file_list'
    api_exportdownload = '/api/export/download'
    api_tbexportfile = '/api/export/tb_file'

    api_excelreplaceone = '/api/excel/replace_one'
    api_excelreplace = '/api/excel/replace'
    api_excelappend = '/api/excel/append'
    api_excelappendbatch = '/api/excel/append_batch'
    api_exceltitlecheck = '/api/excel/title_check'
    api_allcreate = '/api/view/allcreate'
    api_allpreview = '/api/view/allpreview'
    api_aggrfields = '/api/data_aggr/fields'
    api_sqlcheck = '/api/sql_script/check'
    api_allmodify = '/api/view/allmodify'
    api_wbmodify = '/api/wb/modify'
    api_wb_export = '/api/wb/profile_export'
    api_sqlformat = '/api/sql_script/format'
    api_chartmodify_tb = '/api/chart/modify_tb'
    api_viewinfo = '/api/view/info'

    api_chartcreate = '/api/chart/create'
    api_dshmodify = '/api/dashboard/modify'
    api_dshcreate = '/api/dashboard/create'
    api_dshorder = '/api/dashboard/order'
    api_dshmove = '/api/dashboard/move'
    api_chartdelete = '/api/chart/delete'
    api_projecttree = '/api/project/tree'
    api_projectdelete = '/api/project/delete'
    api_projectcreate = '/api/project/create'
    api_projectmove = '/api/project/move'
    api_chartdata = '/api/chart/data'
    api_folderdelete = '/api/folder/delete'
    api_folderlist = '/api/folder/list'
    api_foldertree = '/api/folder/get_tree_with_tblist'
    api_folderchange = '/api/folder/change'
    api_foldercreate = '/api/folder/create'
    api_foldermodifyparent = '/api/folder/modify_parent'
    api_foldermodify = '/api/folder/modify'
    api_foldermodifyseq = '/api/folder/modify_seq'
    api_folderbatchchange = '/api/folder/change_batch'
    api_currenttb = '/api/folder/get_current_tb'
    api_allfoldername = '/api/folder/get_tree'
    api_foldercontaintb = '/api/folder/list_only_tb'
    api_folderfilter = '/api/folder/filter'
    api_dslist = '/api/ds/list'
    api_dsdelete = '/api/ds/delete'
    api_dscreate = '/api/ds/create'
    api_dscdstb = '/api/ds/cdstb'
    api_dssheet = '/api/ds/sheet'
    api_dstask = '/api/ds/task'
    api_dsconn = '/api/ds/conn'
    api_dsinfo = '/api/ds/info'
    api_dsfielddel = '/api/ds_field/field_del'
    api_dsmodify = '/api/ds/modify'
    api_dssync = '/api/ds/sync'
    api_dsopen = '/api/ds_open/deal_token'
    api_dstblist = '/api/ds/tblist'
    api_nslist = '/api/ds/nslist'
    api_usersync = '/api/ds/usersync'
    api_dsrename = '/api/ds/rename'
    api_dsallot = '/api/ds/dsallot'
    api_dsoplog = '/api/ds/oplog'

    api_chartcopy = '/api/chart/copy'
    api_chartinfo = '/api/chart/info'
    api_chartsearch = '/api/chart/search'
    api_chartbdinfo = '/api/chart/database_info'
    api_advdatelist = '/api/adv_date/list'
    api_tbinfo = '/api/tb/info'
    api_dategranularitylist = '/api/date_granularity/list'
    api_dategranularitycommit = '/api/date_granularity/commit'
    api_fieldrange = '/api/field/range'
    api_fieldinnerrange = '/api/field/inner_range'
    api_fieldcreate = '/api/field/create'
    api_fieldmodify = '/api/field/modify'
    api_fielddelete = '/api/field/delete'
    api_fielditemsearch = '/api/field/item_search'
    api_fieldvalidate = '/api/field/item_validate'
    api_fieldlength = '/api/field/get_length'
    api_enumlist = '/api/adv_enum/list'
    api_advenummodify = '/api/adv_enum/modify'
    api_advenumdelete = '/api/adv_enum/delete'
    api_advenumsearch = '/api/adv_enum/search'
    api_advnummodify = '/api/adv_num/modify'
    api_advdatemodify = '/api/adv_date/modify'
    api_chartmodify = '/api/chart/modify'
    api_chartmove = '/api/chart/move'
    api_dshfilteritem = '/api/dsh_filter/item'
    api_mobdshfilteritem = '/mob/dsh_filter/item'
    api_dshfilterlist = '/api/dsh_filter/list'
    api_dshfiltercommit = '/api/dsh_filter/commit'
    api_dashboardinfo = '/api/dashboard/info'
    api_dashfilterrange = '/api/dsh_filter/range'
    api_dashfilterenumsearch = '/api/dsh_filter/enum_search'
    api_fieldgroupexprverify = '/api/field/group_expr_verify'
    api_enumorderinfo = '/api/enum_order/info'
    api_enumorderupdate = '/api/enum_order/update'
    api_dashdelete = '/api/dashboard/delete'
    api_advdatedel = '/api/adv_date/del'
    api_tablecopy = '/api/data_union/union_copy'
    api_dashcopy = '/api/dashboard/copy'
    api_paramrange = '/api/param/range'
    api_paramcreate = '/api/param/create'
    api_paramlist = '/api/param/list'
    api_paramdelete = '/api/param/delete'
    api_parammodify = '/api/param/modify'

    api_partset = '/api/tb/partition/set'
    api_partrm = '/api/tb/partition/remove'
    api_fieldselectedmodify = '/api/tb/field_selected/modify'
    api_fieldenumfilter = '/api/field/filter'
    api_enumcolorfieldrange = '/api/enum_color/field_range'
    api_chartsizegroups = '/api/chart/size_groups'
    api_gistransfer = '/api/gis/transfer'
    api_tbmodifytag = '/api/tb/modify_tag'
    api_chartdelrelatb = '/api/chart/del_rela_tb'
    api_chartaddrelatb = '/api/chart/add_rela_tb'
    api_tbrelalist = '/api/tb/rela_list'
    api_chartfiltercmpdaterange = '/api/chart/filter_cmp_date_range'

    api_tbupdate_mode_modify = '/api/tb/update_mode/modify'
    api_tbupdate_mode_check = '/api/tb/update_mode/check'
    api_warnadd = '/api/warn/add'
    api_warnmodify = '/api/warn/modify'
    api_warndelete = '/api/warn/delete'
    api_warnswitch = '/api/warn/switch'

    api_tbeditable_schema = '/api/tb/editable_schema'
    api_share_alllist = '/api/share/all_list'
    api_share_modify = '/api/share/modify'
    api_wbreplace_check = '/api/wb/replace_check'

    api_openchartdata = '/api/open/chart_data'

    api_chartlinkinfo = '/api/chart_link/info'
    api_chartlinkcommit = '/api/chart_link/commit'
    api_chartlinkdelete = '/api/chart_link/delete'
    api_enum_orderfilter_info = '/api/enum_order/filter_info'
    api_tb_shareinfo = '/api/tb/share_info'
    api_usermodifyinfo = '/api/user/modify_info'
    api_adv_date_scheme_create = '/api/adv_date_scheme/create'
    api_adv_date_scheme_delete = '/api/adv_date_scheme/delete'
    api_adv_date_scheme_modify = "/api/adv_date_scheme/modify"
    api_adv_date_scheme_list = "/api/adv_date_scheme/list"

    # instance global
    _sdk_instance = None

    mobapi_chartdata = '/mob/chart/data'
    mobapi_chartsearch = '/mob/chart/new_search'

    chart_type = {
        "C200": "Table",
        "C210": "Bar Chart",
        "C211": "Stacked Bar Chart",
        "C212": "Percentage Stacked Bar Chart",
        "C220": "Line Chart",
        "C230": "Pie Chart",
        "C240": "Horizontal Bar Chart",
        "C241": "Stacked Horizontal Bar Chart",
        "C242": "Percentage Stacked Horizontal Bar Chart",
        "C250": "Double Axis Chart",
        "C261": "Gauge Chart",
        "C271": "Area Map",
        "C272": "Bubble Map",
        "C280": "Scatter Chart",
        "C290": "Radar Chart",
        "C300": "Sankey Chart",
        "C310": "KPI Card",
        "C320": "WaterFall",
        "C330": "Funnel Chart",
        "C340": "Word Cloud",
        "C350": "Area Chart",
        "C351": "Stacked Area Chart",
        "C352": "Percentage Stacked Area Chart",
        "C360": "Sunburst Chart"
    }

    def __init__(self):
        self.raw_data = {}
        self.user_agent = "BdpAuto_v1.8 Chrome/63.0.3239.132"
        self.user_name = ""
        self.http_request = BDPRequest(bdpconf.BDP_HOST, bdpconf.BDP_PORT)
        # add headers
        self.http_request.add_header("User-Agent", self.user_agent)
        self.http_request.add_header("Content-Type", "application/x-www-form-urlencoded;charset=UTF-8")
        self.dsh_meta = {}
        self.dsh_info = {}
        self.trace_id = ""

    # accounts
    @dec_log()
    def groupcreate(self, name, pid):
        req_param = {
            "_t": time.time(),
            "name": name,
            "parent_group_id": pid
        }
        req_url = self.build_url(self.api_groupcreate, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    @dec_log()
    def groupmodify(self, gid,  **kwargs):
        req_param = {
            "_t": time.time(),
            "group_id": gid
        }

        for k, v in kwargs.iteritems():
            if not (isinstance(v, str) or isinstance(v, unicode)):
                kwargs[k] = json.dumps(v)
        req_param.update(kwargs)
        req_url = self.build_url(self.api_groupmodify, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    @dec_log()
    def grouplist(self):
        req_param = {
            "_t": time.time(),

        }
        req_url = self.build_url(self.api_grouplist, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    @dec_log()
    def groupinfo(self, group_id):
        req_param = {
            "_t": time.time(),
            "group_id": group_id
        }
        req_url = self.build_url(self.api_groupinfo, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    @dec_log()
    def usercreate(self, data):
        assert isinstance(data, dict)
        if isinstance(data, dict):
            data = json.dumps(data)
        req_param = {
            "_t": time.time(),
            "data": data
        }
        req_url = self.build_url(self.api_usercreate, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    @dec_log()
    def usermodify(self,uid, data):
        assert isinstance(data, dict)
        if isinstance(data, dict):
            data = json.dumps(data)
        req_param = {
            "_t": time.time(),
            "sub_id": uid,
            "data": data
        }
        req_url = self.build_url(self.api_usermodify, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    @dec_log()
    def funcmodify(self,uid, data):
        assert isinstance(data, dict)
        if isinstance(data, dict):
            data = json.dumps(data)
        req_param = {
            "_t": time.time(),
            "sub_id": uid,
            "data": data
        }
        req_url = self.build_url(self.api_funcmodify, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    @dec_log()
    def user_reset_pwd(self, sub_id):
        req_param = {
            "_t": time.time(),
            "sub_user_id": sub_id
        }
        req_url = self.build_url(self.api_userreset_pwd, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    @dec_log()
    def subinfo(self, sub_id):
        req_param = {
            "_t": time.time(),
            "sub_id": sub_id
        }
        req_url = self.build_url(self.api_subinfo, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    @dec_log()
    def userinit(self, sub_id, password):
        req_param = {
            "sub_id": sub_id,
            "password": password,
            "rpwd": password
        }
        req_url = self.build_url(self.api_userinit, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    @dec_log()
    def userdel(self, sub_id):
        req_param = {
            "_t": time.time(),
            "session_id": time.time(),
            "sub_id": sub_id,
            "verify_code": ""
        }
        req_url = self.build_url(self.api_userdel, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    @dec_log()
    def userfrozen(self, sub_id_list, is_frozen):
        assert isinstance(sub_id_list, list)
        if isinstance(sub_id_list, list):
            sub_id_list = json.dumps(sub_id_list)
        req_param = {
            "_t": time.time(),
            "sub_id_list": sub_id_list,
            "is_frozen": is_frozen
        }
        req_url = self.build_url(self.api_userfrozen, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    def islogin(self):

        self.userinfo()
        if json.loads(self.raw_data)["status"] != "0":
            return False

        if not json.loads(self.raw_data)["result"]:
            return False

        return True

    @classmethod
    def instance(cls):
        if not cls._sdk_instance:
            cls._sdk_instance = BdpSDK()
            cls._sdk_instance.login(bdpconf.BDP_USER, bdpconf.BDP_PASS, bdpconf.BDP_DOMAIN, update_token=True)
            assert cls._sdk_instance.islogin()

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

    def build_url(self, url, params={}):

        self.trace_id = "ironman_%s" % uuid.uuid3(uuid.NAMESPACE_DNS,
                                                  "%s_%s_%s" % (url, time.time(), randint(0, 100000)))

        params["trace_id"] = self.trace_id

        assert isinstance(params, dict)
        now_time = time.time()
        ms_str = str(int((now_time - long(now_time)) * 1000))
        now_time_str = time.strftime("%F %T", time.localtime(now_time)) + "," + ms_str
        print "[%s]\t[%s]\t[%s]" % (now_time_str, url, params["trace_id"])

        return "%s?%s" % (url, urlencode(params))

    """
    调用指定的接口，然后调用task_status查询结果，最后返回指定字段
    """

    def call_method_and_query(self, method_name, *args, **kwargs):
        self.call_method_and_succ(method_name, *args)
        resp = json.loads(self.raw_data)
        if "task_field" not in kwargs:
            task_id = resp["result"]["task_id"]
        else:
            task_id = eval("resp" + kwargs["task_field"])

        if task_id:
            assert task_id.startswith("task_")
            ts = bdpconf.TIME_OUT

            while ts > 0 and task_id and self.task_status(task_id) in [0, 3]:
                time.sleep(1)
                ts -= 1
            resp_dict = json.loads(self.raw_data)
            if resp_dict["result"]["status"] != 1:
                print "now status: %s" % json.dumps(resp_dict, ensure_ascii=False)
            assert resp_dict["result"]["status"] == 1
        else:
            log.getlog().debug("task_id is %s" % task_id)

        # is return needed?
        if "expect_field" in kwargs:
            return resp_dict["result"][kwargs["expect_field"]]
        elif "expr_val" in kwargs:
            expr_val = kwargs["expr_val"]
            return eval("resp_dict" + expr_val)

    def call_method_and_query_ex_all_succ(self, method_name, *args, **kwargs):
        self.call_method_and_succ(method_name, *args)
        resp = json.loads(self.raw_data)
        if "task_field" not in kwargs:
            if type(resp["result"]) == list:
                for i in resp["result"]:
                    assert i["status"] == 0
                task_ids = [i["task_id"] for i in resp["result"]]
            else:
                task_ids = [resp["result"]["task_id"]]
        else:
            task_ids = eval("resp" + kwargs["task_field"])

        assert len(filter(lambda x: x.startswith("task_"), task_ids)) == len(task_ids)

        ts = bdpconf.TIME_OUT
        isvalid = True
        task_stat_list = zip(task_ids, self.task_status_ex(task_ids))

        while ts > 0 and len(task_stat_list) > 0 and isvalid:
            task_stat_list = zip([i[0] for i in task_stat_list], self.task_status_ex([i[0] for i in task_stat_list]))
            task_stat_list = filter(lambda x: x[1] != 1, task_stat_list)
            invalid_list = filter(lambda x: x[1] not in (0, 3), task_stat_list)
            isvalid = len(invalid_list) == 0
            if isvalid:
                log.getlog().warning("task has invalid status,[(task_id, status)]: %r" % invalid_list)

            time.sleep(1)
            ts -= 1
        self.task_status_ex(task_ids)
        resp_dict = json.loads(self.raw_data)

        # is return needed?
        if "expect_field" in kwargs:
            return resp_dict["result"][kwargs["expect_field"]]
        elif "expr_val" in kwargs:
            expr_val = kwargs["expr_val"]
            return eval("resp_dict" + expr_val)

    def call_method_and_succ(self, method_name, *args, **kwargs):
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            if callable(method):
                method(*args)
                resp = json.loads(self.raw_data)

                if resp["status"] != "0":
                    print "call_method_and_succ resp: %s" % json.dumps(resp, ensure_ascii=False)
                assert resp["status"] == "0"
                if "result" in resp and isinstance(resp["result"], unicode):
                    # print args
                    assert resp["result"] != u"failed"
                if "ret_expr" in kwargs:
                    return eval("resp" + kwargs['ret_expr'])
            else:
                log.getlog().warning("attribute[%s] not callable" % method_name)
        else:
            log.getlog().warning("function %s not found" % method_name)

    def update_dsh_meta(self, dsh_id):
        rst = self.call_method_and_succ(
            "dashboard_info",
            time.time(),
            dsh_id,
            ret_expr='["result"]'
        )
        self.dsh_meta = rst["meta"]
        self.dsh_info = rst

    def generate_single_dsh_meta(self):
        row = 0
        dom_id = "id1"
        if self.dsh_meta and "charts" in self.dsh_meta and len(self.dsh_meta["charts"]) > 0:
            row = self.dsh_meta["charts"][-1]["row"] + self.dsh_meta["charts"][-1]["sizeY"]
            dom_id = "id" + str(len(self.dsh_meta["charts"]) + 1)
        dsh_meta = {
            "row": row,
            "sizeX": 6,
            "sizeY": 4,
            "col": 0,
            "children": [
                {
                    "dom_id": dom_id,
                    "meta": {
                        # "dash_setting": {
                        #     "show_total": True,
                        #     "border_right": False,
                        #     "show_legend": True,
                        #     "border_top": False,
                        #     "show_axis": True,
                        #     "show_title": True,
                        #     "show_datalabels": False,
                        #     "border_null": True,
                        #     "border_bottom": False,
                        #     "border_left": False
                        # },
                        "ct_id": "init_ctid",
                    }
                }
            ],
        }

        return dsh_meta

    def generate_drill_meta(self, drill_fields, y_field):

        meta = self.generate_empty_tb_meta()
        assert isinstance(drill_fields, list)

        for d in drill_fields:
            meta["meta"]["level_fields"].append(
                {
                    "fid": d["fid"],
                    "name": d["f_name"],
                    "data_type": d.type_str(),
                    "is_new": False,
                    "granularity": "day"
                }
            )

        meta["meta"]["level"] = [
            {
                "chart_type": "C210",
                "x": [a],
                "y": [{
                    "fid": y_field["fid"],
                    "uniq_id": int(time.time()*1000000),
                    "name": y_field["f_name"],
                    "data_type": y_field.type_str(),
                    "is_new": False,
                    "is_build_aggregated": y_field.is_build_aggregated(),
                    "aggregator": "SUM",
                    "aggregator_name": u"求和",
                    "alias_name": y_field["f_name"] + u"(求和)",
                    "formatter": {
                        "check": "num",
                        "num": {"digit": 2}
                    },

                }],

                "sort": {
                    "axis": "y",
                    "type": "asc",
                    "fid": y_field["fid"],
                    "col_index": 0
                }
            }
            for a in meta["meta"]["level_fields"]
        ]

        return meta

    def generate_multi_xy_meta(self, x_fields, y_fields):

        meta = self.generate_empty_tb_meta()
        assert isinstance(x_fields, list)
        assert isinstance(y_fields, list)

        for x in x_fields:
            meta["meta"]["level"][0]["x"].append({
                "fid": x["fid"],
                "name": x["f_name"],
                "data_type": x.type_str(),
                "is_new": False if not x.is_build_aggregated() else True,
                "granularity": x["granularity"] if "granularity" in x else "day",
                "granularity_name": x["granularity_name"] if "granularity_name" in x else "",
                "uniq_id": int(time.time() * 1000000),
            })

        for y in y_fields:
            meta["meta"]["level"][0]["y"].append({
                "fid": y["fid"],
                "uniq_id": int(time.time() * 1000000),
                "name": y["f_name"],
                "data_type": y.type_str(),
                "is_new": False if not y.is_build_aggregated() else True,
                "is_build_aggregated": y.is_build_aggregated(),
                "aggregator": self._get_aggregator(y),
                "aggregator_name": u"求和",
                "alias_name": y["f_name"] + u"(求和)",
                "formatter": {
                    "check": "num",
                    "num": {"digit": 2}
                },

            })

        return meta

    def generate_empty_tb_meta(self):
        meta_data = {
            "meta": {
                "filter_list": [],
                "filter_list_inner": [],
                "level_fields": [],
                "level": [
                    {
                        "chart_type": "C200",
                        # "map": {"granularity": "province", "region": 1},
                        "sort": {},
                        "tb_statistic": {
                            "classify": False,
                            "col": False,
                            "row": False
                        },
                        "title_formula": "TOTAL",
                        "type_optional": ["C210", "C220"],
                        "show_y_axis_optional": False,
                        "y": [],
                        "x": [],
                        "yaxis_max": 0,
                        "yaxis_max_disabled": True,
                        "yaxis_min": 0,
                        "yaxis_min_disabled": True,
                    }
                ]
            },
            # "tb_id": tb.tb_id(),
            "description": "",
        }
        return meta_data

    def generate_tb_meta(self, x_field, y_field, *args):

        y = {
            "fid": y_field["fid"],
            "uniq_id": int(time.time() * 1000000),
            "name": y_field["f_name"],
            "data_type": y_field.type_str(),
            "is_new": False,
            "is_build_aggregated": y_field.is_build_aggregated(),
            "aggregator": "SUM",
            "aggregator_name": u"求和",
            "alias_name": y_field["f_name"] + u"(求和)",
            "formatter": {
                "check": "num",
                "num": {"digit": 2}
            },
        }

        x = {
            "fid": x_field["fid"],
            "name": x_field["f_name"],
            "data_type": x_field.type_str(),
            "is_new": False,
            "granularity": "day"
        }

        # meta_data = self.generate_empty_tb_meta()
        meta_data = {
            "meta": {
                "filter_list": [],
                "filter_list_inner": [],
                "level_fields": [],
                "level": [
                    {
                        "chart_type": "C210",
                        "map": {"granularity": "province", "region": 1},
                        # "sort": {
                        #     "type": 'asc',
                        #     "fid": y_field["fid"]
                        # },

                        "sort": {
                            # 2016-08-22暂时删除自动排序,后端存在问题,暂时修改case为:维度为日期手动按日期排序,待后端修复恢复为维度为日期数值排序无效,始终按日期排序

                        } if x_field.type_str() == "date" else {
                            # 2016-08-22暂时删除自动排序,后端存在问题,暂时注释掉,待后端修复恢复为维度为日期数值排序无效,始终按日期排序
                            "axis": 'y',
                            "type": 'asc',
                            "fid": y_field["fid"]
                        },
                        "tb_statistic": {
                            "classify": False,
                            "col": False,
                            "row": False
                        },
                        "title_formula": "TOTAL",
                        "type_optional": ["C210", "C220"],
                        "show_y_axis_optional": False,
                        "y": [y],
                        "x": [x],
                        "yaxis_max": 0,
                        "yaxis_max_disabled": True,
                        "yaxis_min": 0,
                        "yaxis_min_disabled": True,
                        "tb_sort": {},

                    }
                ]
            },
            # "tb_id": tb.tb_id(),
            "description": "",
        }
        return meta_data

    def generate_c200_meta(self, x_field, y_field, *args):

        y = {
            "fid": y_field["fid"],
            "uniq_id": int(time.time() * 1000000),
            "name": y_field["f_name"],
            "data_type": y_field.type_str(),
            "is_new": False,
            "is_build_aggregated": y_field.is_build_aggregated(),
            "aggregator": "SUM",
            "aggregator_name": u"求和",
            "alias_name": y_field["f_name"] + u"(求和)",
            "formatter": {
                "check": "num",
                "num": {"digit": 2}
            },
        }

        x = {
            "fid": x_field["fid"],
            "name": x_field["f_name"],
            "data_type": x_field.type_str(),
            "is_new": False,
            "granularity": "day"
        }

        # meta_data = self.generate_empty_tb_meta()
        meta_data = {
            "meta": {
                "filter_list": [],
                "filter_list_inner": [],
                "level_fields": [],
                "level": [
                    {
                        "chart_type": "C200",
                        "map": {"granularity": "province", "region": 1},
                        "tb_statistic": {
                            "classify": False,
                            "col": False,
                            "row": False
                        },
                        "title_formula": "TOTAL",
                        "type_optional": ["C210", "C220"],
                        "show_y_axis_optional": False,
                        "y": [y],
                        "x": [x],
                        "yaxis_max": 0,
                        "yaxis_max_disabled": True,
                        "yaxis_min": 0,
                        "yaxis_min_disabled": True,
                        "tb_sort": {},

                    }
                ]
            },
            # "tb_id": tb.tb_id(),
            "description": "",
        }
        return meta_data

    def _get_aggregator(self, y_field):

        if y_field.type_str() == "number":
            if "aggregator" in y_field:
                if y_field["aggregator"] in (
                        "SUM", "AVG", "AVERAGE", "COUNT", "COUNT_DISTINCT", "MAX", "MIN", "PERCENT"):
                    return y_field["aggregator"]
                else:
                    return "SUM"
            elif y_field.is_build_aggregated() == 1:
                return ""
            else:
                return "SUM"

        elif y_field.type_str() in ("date", "string"):
            if "aggregator" in y_field and y_field["aggregator"] in ("COUNT", "COUNT_DISTINCT"):
                return y_field["aggregator"]
            else:
                return "COUNT"
        else:
            assert False

    def generate_meta(self, chart_type="C200", x_axis=[], compare_axis=[], y_axis=[], y_optional_axis=[]):

        meta = self.generate_multi_xy_meta(x_axis, y_axis)

        meta["meta"]["level"][0]["chart_type"] = chart_type

        for index, y_field in enumerate(y_axis):
            meta["meta"]["level"][0]["y"][index]["aggregator"] = self._get_aggregator(y_field)

        if compare_axis:
            meta["meta"]["level"][0]["compare_axis"] = []
            for x_field in compare_axis:
                meta["meta"]["level"][0]["compare_axis"].append(
                    {
                        "fid": x_field["fid"],
                        "name": x_field["f_name"],
                        "data_type": x_field.type_str(),
                        "is_new": False if not x_field.is_build_aggregated() else True,
                        "granularity": x_field["granularity"] if "granularity" in x_field else "day",
                        "granularity_name": x_field["granularity_name"] if "granularity_name" in x_field else "",
                        "uniq_id": int(time.time() * 1000000),
                    }
                )

        if y_optional_axis:
            meta["meta"]["level"][0]["y_optional"] = []
            for y_field in y_optional_axis:
                meta["meta"]["level"][0]["y_optional"].append(
                    {
                        "fid": y_field["fid"],
                        "uniq_id": int(time.time() * 1000000),
                        "name": y_field["f_name"],
                        "data_type": y_field.type_str(),
                        "is_new": False if not y_field.is_build_aggregated() else True,
                        "is_build_aggregated": y_field.is_build_aggregated(),
                        "aggregator": self._get_aggregator(y_field),
                        "aggregator_name": u"nop",
                        "alias_name": y_field["f_name"] + u"nop",
                        "formatter": {
                            "check": "num",
                            "num": {"digit": 2}
                        },
                    }
                )

            meta["meta"]["level"][0]["show_y_axis_optional"] = True if meta["meta"]["level"][0]["y_optional"] else False

        return meta

    def _layer_meta(self, layer_tb_id):

        layer_meta = {
            "tb_id": layer_tb_id,
            "layer_name": "layer_name_%s" % time.time(),
            "layer_id": "layer_%s" % (time.time() * 1000000),
            "lng": [],
            "lat": [],
            "x": [],
            "y": [],
            "type": "bubble",
            "bubble_symbol": "circle",
            "filter_list": [],
            "filterRangeList": {}
        }
        return layer_meta

    def generate_gis_empty_meta(self):

        meta = {
            "name": u"未命名图表",
            "meta": {
                "chart_type": "C400",
                "zoom": 8,
                "center": [90.947443, 41.723343],
                "layers": []
            },
        }

        return meta

    def generate_gis_single_layer_meta(self, tb_id="", lat=None, lng=None, layer_type="bubble", bubble_symbol="circle",
                                       x_axis=[], compare_axis=[], y_axis=[], y_optional_axis=[]):

        assert layer_type in ("bubble", "heatmap", "massive", "graph", "trajectory", "d_trajectory")
        assert bubble_symbol in ("circle",)
        layer_mata = self._layer_meta(tb_id)

        assert isinstance(x_axis, list)
        assert isinstance(y_axis, list)
        assert isinstance(compare_axis, list)
        assert isinstance(y_optional_axis, list)

        layer_mata["type"] = layer_type
        layer_mata["bubble_symbol"] = bubble_symbol

        if lat:
            layer_mata["lat"] = {
                "is_build_aggregated": lat.is_build_aggregated(),
                "fid": lat["fid"],
                "data_type": lat.type_str(),
                "name": lat["f_name"],
            }
        if lng:
            layer_mata["lng"] = {
                "is_build_aggregated": lng.is_build_aggregated(),
                "fid": lng["fid"],
                "data_type": lng.type_str(),
                "name": lng["f_name"],
            }

        for x in x_axis:
            layer_mata["x"].append({
                "fid": x["fid"],
                "name": x["f_name"],
                "data_type": x.type_str(),
                "is_new": False if not x.is_build_aggregated() else True,
                "granularity": x["granularity"] if "granularity" in x else "day",
                "granularity_name": x["granularity_name"] if "granularity_name" in x else "",
                "uniq_id": int(time.time() * 1000000),
            })

        for y in y_axis:
            layer_mata["y"].append({
                "fid": y["fid"],
                "uniq_id": int(time.time() * 1000000),
                "name": y["f_name"],
                "data_type": y.type_str(),
                "is_new": False if not y.is_build_aggregated() else True,
                "is_build_aggregated": y.is_build_aggregated(),
                "aggregator": self._get_aggregator(y),
                "aggregator_name": u"求和",
                "alias_name": y["f_name"] + u"(求和)",
                "formatter": {
                    "check": "num",
                    "num": {"digit": 2}
                },
            })

        if compare_axis:
            layer_mata["compare_axis"] = []
            for x_field in compare_axis:
                layer_mata["compare_axis"].append(
                    {
                        "fid": x_field["fid"],
                        "name": x_field["f_name"],
                        "data_type": x_field.type_str(),
                        "is_new": False if not x_field.is_build_aggregated() else True,
                        "granularity": x_field["granularity"] if "granularity" in x_field else "day",
                        "granularity_name": x_field["granularity_name"] if "granularity_name" in x_field else ""
                    }
                )

        if y_optional_axis:
            layer_mata["y_optional"] = []
            for y_field in y_optional_axis:
                layer_mata["y_optional"].append(
                    {
                        "fid": y_field["fid"],
                        "uniq_id": int(time.time() * 1000000),
                        "name": y_field["f_name"],
                        "data_type": y_field.type_str(),
                        "is_new": False if not y_field.is_build_aggregated() else True,
                        "is_build_aggregated": y_field.is_build_aggregated(),
                        "aggregator": self._get_aggregator(y_field),
                        "aggregator_name": u"nop",
                        "alias_name": y_field["f_name"] + u"nop",
                        "formatter": {
                            "check": "num",
                            "num": {"digit": 2}
                        },
                    }
                )

            layer_mata["show_y_axis_optional"] = True if layer_mata["y_optional"] else False

        return layer_mata

    def generate_gis_meta(self, layers=[]):

        """
        layers example:
        layers = [
            dict(
                tb_id="", lat=None, lng=None, x_axis=[], compare_axis=[], y_axis=[], y_optional_axis=[]
            ),
            dict(
                tb_id="", lat=None, lng=None, x_axis=[], compare_axis=[], y_axis=[], y_optional_axis=[]
            )
        ]
        """

        assert isinstance(layers, list)

        meta = self.generate_gis_empty_meta()

        for layer in layers:
            assert isinstance(layer, dict)
            meta["meta"]["layers"].append(
                self.generate_gis_single_layer_meta(**layer)
            )

        return meta

    def generate_c300_meta(self, x1_field, x2_field, y_field, r_field, *args):

        y = {
            "fid": y_field["fid"],
            "uniq_id": int(time.time() * 1000000),
            "name": y_field["f_name"],
            "data_type": y_field.type_str(),
            "is_new": False,
            "is_build_aggregated": y_field.is_build_aggregated(),
            "aggregator": "COUNT",
            "aggregator_name": u"计数",
            "alias_name": y_field["f_name"] + u"(计数)",
            "formatter": {
                "num": {
                    "digit": 0,
                    "millesimal": True
                },
                "check": "num"
            },
        }

        x1 = {
            "fid": x1_field["fid"],
            "name": x1_field["f_name"],
            "data_type": x1_field.type_str(),
            "is_new": False,
            "is_build_aggregated": x1_field.is_build_aggregated(),
            "granularity": "day"
        }

        x2 = {
            "fid": x2_field["fid"],
            "name": x2_field["f_name"],
            "data_type": x2_field.type_str(),
            "is_new": False,
            "is_build_aggregated": x2_field.is_build_aggregated(),
            "granularity": "day"
        }

        # meta_data = self.generate_empty_tb_meta()
        meta_data = {
            "meta": {
                "filter_list": [],
                "filter_list_inner": [],
                "level_fields": [],
                "level": [
                    {
                        "chart_type": "C300",
                        "sankey_setting": {
                            "relate_field_fid": r_field["fid"]
                        },
                        "title_formula": "",
                        "type_optional": ["C210", "C220"],
                        "show_y_axis_optional": False,
                        "y": [y],
                        "x": [x1, x2],
                        "yaxis_max": 0,
                        "yaxis_max_disabled": True,
                        "yaxis_min": 0,
                        "yaxis_min_disabled": True,
                        "sort": {},
                        "top": {
                            "enabled": False,
                            "reversed": 0,
                            "type": "items",
                            "value": ""
                        },
                        "top_compare": {
                            "type": "items",
                            "reversed": 0,
                            "enabled": False
                        }
                    }
                ]
            },
            # "tb_id": tb.tb_id(),
            "description": "",
        }
        return meta_data

    @classmethod
    def get_week_number(cls, dt):
        first_day = datetime.datetime(day=1, month=1, year=dt.year)
        delta = dt - first_day
        if first_day.isoweekday() == 1:
            return int(math.ceil((delta.days + first_day.isoweekday()) / 7.0))
        else:
            return int(math.ceil((delta.days + first_day.isoweekday()) / 7.0)) - 1

    @dec_log()
    def login(self, username, password, domain, update_token=False):
        req_param = {
            'username': username,
            'password': password,
            'domain': domain
        }

        req_url = self.build_url(self.api_login)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

        if update_token:
            resp = json.loads(self.raw_data)
            assert resp["status"] == "0"
            assert resp["result"]["user_info"]["username"] == username
            # self.access_token = resp["result"]["access_token"]
            self.user_name = resp["result"]["user_info"]["username"]

        if bdpconf.BDP_SMALL_EMULATE:
            cj = self.http_request.bdp_session.cookies
            requests.utils.add_dict_to_cookiejar(cj, dict(domain=bdpconf.BDP_DOMAIN))

    @dec_log()
    def userinfo(self):

        self.raw_data = self.http_request.get(self.build_url(self.api_userinfo)).read()

    def set_locale(self, locale="zh"):

        cj = self.http_request.bdp_session.cookies
        requests.utils.add_dict_to_cookiejar(cj, dict(locale=locale))

    def set_locale_en(self):
        self.set_locale("en")

    def set_locale_zh(self):
        self.set_locale()

    @dec_log()
    def export_excel(self, ct_id, dsh_id):

        boundary = ''.join(random.sample('abcdefgABCDEFG1234567', 16))

        data = list()
        data.append("--%s" % boundary)
        data.append('Content-Disposition: form-data; name="ct_id"\r\n')
        data.append(ct_id)
        data.append("--%s" % boundary)
        data.append('Content-Disposition: form-data; name="dsh_id"\r\n')
        data.append(dsh_id)
        data.append("--%s--\r\n" % boundary)
        # try:
        raw_resp = self.http_request.post(self.build_url(BdpSDK.api_excelexport),
                                          '\r\n'.join(data), stream=True,
                                          headers={"Content-Type": 'multipart/form-data; boundary=%s' % boundary})
        content_disp = raw_resp.headers["Content-Disposition"]
        content_len = int(raw_resp.headers["Content-Length"])

        content_dict = {}
        for i in content_disp.split(';'):
            try:
                k, v = i.split('=')
            except:
                k, v = "", ""

            if k:
                content_dict[k.strip()] = v.strip().strip('"')

        local_file = content_dict["filename"]

        fp = open("%s/%s" % (bdpconf.DOWNLOAD_DIR, local_file), "wb")

        for i in raw_resp.iter_content(chunk_size=4096):
            fp.write(i)

        assert fp.tell() == content_len

        fp.close()

    # 文件上传支持添加辅助字段
    @dec_log()
    def upload_excel(self, excel_file, terminate=',', extra_fields={}):

        if hasattr(excel_file, "read"):
            filename = excel_file.filename
            fp = excel_file
        else:
            filename = os.path.basename(excel_file)
            fp = open(excel_file)

        _map = {
            ',': "comma",
            ';': "semicolon",
            'tab': 'tab',
            ' ': 'space'
        }

        if isinstance(extra_fields, dict):
            extra_fields = json.dumps(extra_fields)

        assert terminate in _map
        boundary = ''.join(random.sample('abcdefgABCDEFG1234567', 16))

        data = list()
        data.append("--%s" % boundary)
        data.append('Content-Disposition: form-data; name="opt"\r\n')
        data.append('1')
        data.append("--%s" % boundary)
        data.append('Content-Disposition: form-data; name="folder_id"\r\n')
        data.append('folder_root')
        data.append("--%s" % boundary)
        data.append('Content-Disposition: form-data; name="field_terminate"\r\n')
        data.append(_map[terminate])
        data.append("--%s" % boundary)
        data.append('Content-Disposition: form-data; name="extra_fields"\r\n')
        data.append(extra_fields)
        data.append("--%s" % boundary)
        data.append('Content-Disposition: form-data; name="file"; filename="%s"' % filename)
        data.append('Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet\r\n')

        data.append(fp.read())
        fp.close()

        data.append("--%s--\r\n" % boundary)

        self.raw_data = self.http_request.post(
            self.build_url(BdpSDK.api_excelupload),
            '\r\n'.join(data),
            headers={"Content-Type": 'multipart/form-data; boundary=%s' % boundary}
        ).read()

    @dec_log()
    def project_tree(self, _t=None, categories=[0, 2]):
        req_param = {
            "_t": _t,
            "categories": categories
        }
        req_url = self.build_url(self.api_projecttree, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    @dec_log()
    def chart_search(self, ct_name, is_tpl=0):
        req_param = {
            "ct_name": ct_name,
            "is_tpl": is_tpl
        }
        req_url = self.build_url(self.api_chartsearch, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    @dec_log()
    def mob_chart_search(self, ct_name, system, app_ver, test_on):
        req_param = {
            "ct_name": ct_name,
            "system": system,
            "app_ver": app_ver,
            "test": "1" if test_on else "0"
        }
        req_url = self.build_url(self.mobapi_chartsearch, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    @dec_log()
    def get_file_type(self, ct_id, dsh_id, linked_chart_type=0, rule_id=None):
        req_param = {
            "ct_id": ct_id,
            "dsh_id": dsh_id,
            "linked_chart_type": linked_chart_type,
            "rule_id": rule_id
        }
        req_url = self.build_url(self.api_getfiletype)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def export_large_file(self, ct_id, dsh_id, linked_chart_type=0, rule_id=None):
        req_param = {
            "ct_id": ct_id,
            "dsh_id": dsh_id,
            "linked_chart_type": linked_chart_type,
            "rule_id": rule_id
        }
        req_url = self.build_url(self.api_exportlargefile)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def export_table_file(self, tb_id, row_filter={}):
        req_param = {
            "tb_id": tb_id,
            "row_filter": json.dumps(row_filter)
        }

        req_url = self.build_url(self.api_tbexportfile)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @loop_succ
    @dec_log()
    def export_file_list(self, page=1, type=1):
        req_param = {
            "_t": time.time(),
            "page": page,
            "type": type
        }
        req_url = self.build_url(self.api_exportfilelist)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()
        if json.loads(self.raw_data)['result']['files'][0]['status'] == 0:
            return True
        elif json.loads(self.raw_data)['result']['files'][0]['status'] == 1:
            return False

    @dec_log()
    def export_download(self, export_id):
        req_param = {
            "export_id": export_id
        }
        req_url = self.build_url(self.api_exportdownload, req_param)
        raw_resp = self.http_request.get(req_url)

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

        fp = open("%s/%s" % (bdpconf.DOWNLOAD_DIR, local_file), "wb")

        for i in raw_resp.iter_content(chunk_size=4096):
            fp.write(i)

        assert fp.tell() == content_len

        fp.close()

    @dec_log()
    def project_create(self, proj_name, parent_id=''):
        req_param = {
            "name": proj_name,
            "parent_id": parent_id
        }
        req_url = self.build_url(self.api_projectcreate)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def project_delete(self, proj_id):
        req_param = {
            "proj_id": proj_id
        }
        req_url = self.build_url(self.api_projectdelete, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    @dec_log()
    def project_move(self, sortlist, proj_id, parent_id='', owner_type=0):
        req_param = {
            "sort": json.dumps(sortlist),
            "proj_id": proj_id,
            "parent_id": parent_id,
            "type": owner_type
        }
        req_url = self.build_url(self.api_projectmove)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def task_status(self, task_id):
        req_param = {
            "task_id": task_id,
        }
        self.raw_data = self.http_request.get(self.build_url(BdpSDK.api_taskstatus, req_param)).read()
        return json.loads(self.raw_data)["result"]["status"]

    @dec_log()
    def task_status_ex(self, task_ids):
        task_ids_req = ','.join(task_ids) if type(task_ids) == list else task_ids
        req_param = {
            "task_id": task_ids_req,
        }
        self.raw_data = self.http_request.get(self.build_url(BdpSDK.api_taskstatus, req_param)).read()
        result = json.loads(self.raw_data)["result"]
        if len(task_ids) > 1:
            assert set(task_ids) == set([i for i in result.iterkeys()])
            return [result[i]["status"] for i in task_ids]
        else:
            return [result["status"]]

    @dec_log()
    def excel_create(self, excel_id, sheet_names, tb_name, folder_id="folder_root"):
        assert isinstance(sheet_names, list)
        req_param = {
            "excel_id": excel_id,
            "sheet_names": json.dumps(sheet_names),
            "folder_id": folder_id,
            "tb_name": tb_name
        }
        req_url = self.build_url(self.api_excelcreate)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def excel_preview(self, excel_id, udt=[], row_offsets=[], sheet_names=[]):
        req_param = {
            "excel_id": excel_id,
            'udt': json.dumps(udt),
            'row_offsets': json.dumps(row_offsets),
            'sheet_names': json.dumps(sheet_names)
        }
        req_url = self.build_url(self.api_excelpreview)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def excel_parser(self, excel_id, sheet_names, rowoffsets, udt=[]):
        assert isinstance(sheet_names, list)
        assert isinstance(rowoffsets, list)
        req_param = {
            "excel_id": excel_id,
            "sheet_names": json.dumps(sheet_names),
            "row_offsets": json.dumps(rowoffsets),
            'udt': json.dumps(udt)
        }
        req_url = self.build_url(self.api_excelparser)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def excel_tb_schema(self, tb_id):
        req_param = {
            "tb_id": tb_id
        }
        req_url = self.build_url(self.api_excelschema, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    @dec_log()
    def excel_create_folder(self, excel_id, sheet_names, folder_id):
        assert isinstance(sheet_names, list)
        req_param = {
            "excel_id": excel_id,
            "sheet_names": json.dumps(sheet_names),
            "folder_id": folder_id,
        }
        req_url = self.build_url(self.api_excelcreate)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @loop_succ
    @dec_log()
    def table_modify(self, data):
        if not isinstance(data, str):
            data = json.dumps(data)
        req_param = {
            "data": data,
        }
        # pdb.set_trace()
        req_url = self.build_url(self.api_tbmodify)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

        if json.loads(self.raw_data)["status"] in ("0", "19006", "40002"):
            return True
        else:
            return False

    @dec_log()
    def table_preview(self, tb_id, where="", sortopt=""):
        req_param = {
            "tb_id": tb_id
        }

        if where:
            assert isinstance(where, dict)
            req_param["where"] = json.dumps(where)

        if sortopt:
            assert isinstance(sortopt, list)
            req_param["sort"] = json.dumps(sortopt)

        req_url = self.build_url(self.api_tbpreview, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    @dec_log()
    def table_status(self, tb_id):
        req_param = {
            "tb_id": tb_id
        }
        req_url = self.build_url(self.api_tbstatus, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    @dec_log()
    def excel_append(self, excel_id, tb_id, sheet_names, title_map, add_fields, del_fields):
        # assert isinstance(sheet_names, list)
        req_param = {
            "excel_id": excel_id,
            "tb_id": tb_id,
            "sheet_name": sheet_names,
            "tb_title_ex_title_mapping": json.dumps(title_map),
            "add_field_titles": json.dumps(add_fields),
            "del_field_titles": json.dumps(del_fields),
            "force": 1
        }
        req_url = self.build_url(self.api_excelappend)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def excel_replace(self, excel_id, tb_id, sheet_names, title_map, add_fields, del_fields):
        req_param = {
            "excel_id": excel_id,
            "tb_id": tb_id,
            "sheet_name": sheet_names,
            "tb_title_ex_title_mapping": json.dumps(title_map),
            "add_field_titles": json.dumps(add_fields),
            "del_field_titles": json.dumps(del_fields),
            "force": 1
        }
        req_url = self.build_url(self.api_excelreplace, req_param)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def excel_list(self, tb_id, _t=""):
        req_param = {
            "time": _t,
            "tb_id": tb_id
        }
        req_url = self.build_url(self.api_excellist, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    @dec_log()
    def excel_delete(self, map_id, tb_id, _t=""):
        req_param = {
            "_t": _t,
            "map_id": map_id,
            "tb_id": tb_id
        }
        req_url = self.build_url(self.api_exceldelete, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    @dec_log()
    def allpreview(self, info, generator_type):

        assert isinstance(info, dict)

        req_param = {
            "info": json.dumps(info),
            "generator_type": generator_type,
        }
        req_url = self.build_url(self.api_allpreview)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def aggrfields(self, tb_id):

        req_param = {
            "_t": time.time(),
            "tb_id": tb_id,
        }
        req_url = self.build_url(self.api_aggrfields)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def sql_check(self, sql):
        req_param = {
            "sql": sql,
        }

        req_url = self.build_url(self.api_sqlcheck)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    def allcreate(self, info, generator_type, folder=""):

        if isinstance(info, dict):
            info = json.dumps(info)

        if folder:
            assert folder.startswith("folder_")
        else:
            folder = "folder_root"

        req_param = {
            "info": info,
            "generator_type": generator_type,
            "folder_id": folder
        }
        req_url = self.build_url(self.api_allcreate)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def viewinfo(self, type, tb_id):

        req_param = {
            "type": type,
            "tb_id": tb_id,
        }
        req_url = self.build_url(self.api_viewinfo)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    def allmodify(self, info, tb_id, folder="", generator_type=""):
        #generator_type = {0: 关联表, 1: 聚合表, 2: 追加表, 3: sql合表, 7: 二维转一维}

        if isinstance(info, dict):
            info = json.dumps(info)

        if folder:
            assert folder.startswith("folder_")
        else:
            folder = "folder_root"

        req_param = {
            "info": info,
            "tb_id": tb_id,
            "folder_id": folder,
            "generator_type": generator_type,
        }
        req_url = self.build_url(self.api_allmodify)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def table_delete(self, tb_id):
        req_param = {
            "tb_id": tb_id
        }
        req_url = self.build_url(self.api_tbdelete, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    def _add_to_dsh(self, ct_id, dsh_id):

        data = {
            "name": "dsh_1",
            "meta": {
                "charts": [
                    {
                        "sizeX": 4, "sizeY": 2, "row": 0, "col": 4, "children": [
                        {
                            "dom_id": "id1",
                            "meta": {"ct_id": ct_id}
                        }
                    ]

                    }
                ]
            }
        }

        self.dsh_modify(dsh_id, data)

    @dec_log()
    def chart_create(self, dsh_id, tbid_or_tbids, dsh_meta=None, ct_type=""):

        def _output_ct_id(cstr):

            assert cstr.startswith("ct_")

            with open(bdpconf.CT_CACHE_FILE, "a") as fp:
                fp.seek(0, 2)
                fp.write("%s\n" % cstr)

        if dsh_meta:
            assert isinstance(dsh_meta, dict)
            real_dsh_meta = dsh_meta
        else:
            self.update_dsh_meta(dsh_id)
            real_dsh_meta = {}
            real_dsh_meta.update(
                {"charts": self.dsh_meta["charts"] if self.dsh_meta and "charts" in self.dsh_meta else []})
            for i in range(len(real_dsh_meta["charts"])):
                ct_id_tmp = real_dsh_meta["charts"][i]["children"][0]["meta"]["ct_id"]
                real_dsh_meta["charts"][i]["children"][0]["meta"] = {"ct_id": ct_id_tmp}

            real_dsh_meta["charts"].append(self.generate_single_dsh_meta())

        req_param = {
            "dsh_id": dsh_id,
        }
        if ct_type == "1":  # gis
            req_param["tb_ids"] = json.dumps(tbid_or_tbids)
            req_param["ct_type"] = ct_type
        else:  # 非gis
            req_param["tb_id"] = tbid_or_tbids

        if real_dsh_meta:
            req_param["dsh_meta"] = json.dumps(real_dsh_meta)

        req_url = self.build_url(self.api_chartcreate)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

        _resp = json.loads(self.raw_data)

        # print _resp  # case失败后便于跟踪排查问题
        if _resp["status"] == "0":
            _output_ct_id(_resp["result"]["ct_id"])

    @dec_log()
    def folder_list(self):
        req_param = {
            "_t": time.time()
        }
        req_url = self.build_url(self.api_folderlist, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    @dec_log()
    def folder_tree(self, get_first=1, get_root=1, tb_list=[]):
        req_param = {
            "_t": time.time(),
            "get_first": get_first,
            "get_root": get_root,
            "tb_list": json.dumps(tb_list)
        }
        req_url = self.build_url(self.api_foldertree, req_param)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def folder_change(self, tb_id, to_folder="folder_root", tb_index=0, to_seq=0):
        req_param = dict(
            tb_id=tb_id,
            tb_index=tb_index,
            to_seq=to_seq
        )

        if to_folder != "folder_root":
            req_param["to_folder"] = to_folder

        req_url = self.build_url(self.api_folderchange, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    @dec_log()
    def folder_delete(self, folder_id, delete_mode=0):
        req_param = {
            "folder_id": folder_id,
            "mode": delete_mode,
        }
        req_url = self.build_url(self.api_folderdelete, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    @dec_log()
    def chart_delete(self, ct_id, dsh_meta=None):

        self.chart_info(ct_id)

        if json.loads(self.raw_data)['status'] != '0':
            dsh_id = None
        else:
            dsh_id = json.loads(self.raw_data)["result"]["dsh_id"]

        if dsh_meta and dsh_id:
            assert isinstance(dsh_meta, dict)
            real_dsh_meta = dsh_meta

        elif dsh_id:
            self.update_dsh_meta(dsh_id)
            real_dsh_meta = {}
            real_dsh_meta.update({"charts": self.dsh_meta["charts"] if "charts" in self.dsh_meta else []})
            for i in range(len(real_dsh_meta["charts"])):
                ct_id_tmp = real_dsh_meta["charts"][i]["children"][0]["meta"]["ct_id"]
                real_dsh_meta["charts"][i]["children"][0]["meta"] = {"ct_id": ct_id_tmp}

        else:
            real_dsh_meta = {}

        find_chart = False
        if real_dsh_meta and real_dsh_meta["charts"]:
            for c in real_dsh_meta["charts"]:
                if c["children"][0]["meta"]["ct_id"] == ct_id:
                    real_dsh_meta["charts"].remove(c)
                    find_chart = True
                    break

        req_param = {
            "ct_id": ct_id,
            "dsh_meta": json.dumps(real_dsh_meta) if find_chart else {}
        }

        req_url = self.build_url(self.api_chartdelete)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def dsh_modify(self, dsh_id, data):

        str_data = json.dumps(data) if isinstance(data, dict) else data
        req_param = {
            "_t": int(time.time()) * 1000,
            "dsh_id": dsh_id,
            "data": str_data
        }
        req_url = self.build_url(self.api_dshmodify)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def dsh_create(self, name, proj_id, label='', comment=''):
        req_param = {
            "name": name,
            "proj_id": proj_id,
            "label": label,
            "comment": comment,
            "meta": dict()
        }
        req_url = self.build_url(self.api_dshcreate)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def chart_data(self, ct_id, dsh_id=None, linked_chart_type=None, tb_sort="", filter_ops="", drill_ops="",
                   rule_id="", is_open_chart_data=False, advanced_sort='', linked_value='', display_granularity=None,
                   filter_cmp_date_range=None, free_drill_opt="", param_setting=''):

        # 这里必须把每一个参数都处理成json串，后端不会处理的，这是最后一层
        req_param = {
            "ct_id": ct_id,
            # "dsh_id": dsh_id,
            # "linked_chart_type": linked_chart_type
            "tb_sort": tb_sort,
            # "filter_liet": filter_list,
        }

        # drill options
        real_drill_ops = {}

        if isinstance(drill_ops, dict):
            real_drill_ops = drill_ops

        for a, b in real_drill_ops.items():
            if type(b) in (list, dict):
                req_param[a] = json.dumps(b)
            else:
                req_param[a] = b

        # 有些时候查询是带有过滤器参数的，这里处理一下
        real_filter_ops = {}

        if isinstance(filter_ops, dict):
            real_filter_ops = filter_ops

        for fop, v in real_filter_ops.items():
            req_param[fop] = v if isinstance(v, str) else json.dumps(v)

        # 这里处理排序参数
        if len(tb_sort) == 0:
            req_param.pop("tb_sort")

        if dsh_id:
            req_param["dsh_id"] = dsh_id

        # 模板分配的图表需要rule_id
        if rule_id:
            req_param["rule_id"] = rule_id

        if linked_value:
            req_param["linked_value"] = json.dumps(linked_value)

        if advanced_sort:
            req_param["advanced_sort"] = json.dumps(advanced_sort)
            req_param["is_advanced_sort"] = 1

        # 图表日期粒度切换
        if display_granularity:
            assert isinstance(display_granularity, dict)
            req_param["display_granularity"] = json.dumps(display_granularity)

        # 同比环比对比日期自定义
        if filter_cmp_date_range is not None:
            assert isinstance(filter_cmp_date_range, list)
            req_param["filter_cmp_date_range"] = json.dumps(filter_cmp_date_range)

        # 自由下钻
        if free_drill_opt:
            req_param["free_drill_opt"] = json.dumps(free_drill_opt)

        #  图内参数
        if param_setting:
            assert isinstance(param_setting, list)
            req_param["param_setting"] = json.dumps(param_setting)

        api_name = self.api_chartdata if not is_open_chart_data else self.api_openchartdata
        req_url = self.build_url(api_name)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def chart_info(self, ct_id):
        req_param = {
            "ct_id": ct_id
        }
        req_url = self.build_url(self.api_chartinfo)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def chart_database_info(self, atime, ct_id):
        req_param = {
            "time": atime,
            "ct_id": ct_id
        }
        req_url = self.build_url(self.api_chartbdinfo, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    @dec_log()
    def adv_date_list(self, ct_id, scheme_id):
        req_param = {
            "ct_id": ct_id,
            "scheme_id": scheme_id,
        }
        req_url = self.build_url(self.api_advdatelist)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def adv_date_modify(self, ct_id, opt_id, data, scheme_id, dsh_id="", df_id=""):

        if ct_id:
            assert not dsh_id
            assert not df_id

        req_param = {
            "ct_id": ct_id,
            "opt_id": opt_id,
            "data": json.dumps(data),
            "scheme_id": scheme_id
        }

        if not ct_id:
            del req_param["ct_id"]
            req_param.update(dict(
                dsh_id=dsh_id,
                df_id=df_id
            ))

        req_url = self.build_url(self.api_advdatemodify, )
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def tb_info(self, tb_id, need_param=None, query_for_ct=None):
        req_param = {
            "tb_id": tb_id
        }

        if need_param is not None:
            req_param["need_param"] = need_param

        if query_for_ct is not None:
            req_param["query_for_ct"] = query_for_ct

        req_url = self.build_url(self.api_tbinfo, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    @dec_log()
    def date_granularity_list(self, tb_id):
        req_param = {
            "tb_id": tb_id
        }
        req_url = self.build_url(self.api_dategranularitylist)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def date_granularity_commit(self, tb_id, value):
        req_param = {
            "tb_id": tb_id,
            "data": json.dumps(value)
        }
        req_url = self.build_url(self.api_dategranularitycommit)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def field_range(self, tb_id, fid, ct_id=""):
        req_param = {
            "tb_id": tb_id,
            "fid": fid,
        }

        if ct_id:  # 机器学习中筛选字段不需要传ct_id
            req_param["ct_id"] = ct_id
        req_url = self.build_url(self.api_fieldrange)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def field_inner_range(self, **kwargs):

        for k, v in kwargs.iteritems():
            if not (isinstance(v, str) or isinstance(v, unicode)):
                kwargs[k] = json.dumps(v)

        # dsh_id 为空则删除key
        if "dsh_id" in kwargs and not kwargs["dsh_id"]:
            del kwargs["dsh_id"]

        # 仪表盘模式必传参数
        if "dsh_id" in kwargs:
            if "rule_id" not in kwargs:
                kwargs["rule_id"] = ""

            if "dsh_filter" not in kwargs:
                kwargs["dsh_filter"] = json.dumps([])

        # 仪表盘模式必传参数
        if "dsh_id" in kwargs and "drill_field" not in kwargs or "drill_level" not in kwargs or "drill_value" not in kwargs:
            kwargs.update(
                drill_level="",
                drill_field="",
                drill_value=json.dumps([])
            )
        elif "drill_field" not in kwargs or "drill_level" not in kwargs or "drill_value" not in kwargs:
            if "drill_field" in kwargs:
                del kwargs["drill_field"]
            if "drill_level" in kwargs:
                del kwargs["drill_field"]
            if "drill_value" in kwargs:
                del kwargs["drill_field"]

        # 无论怎样都得传
        if "granularity" not in kwargs:
            kwargs["granularity"] = ""

        # 数值接口为get型,且需要传uniq_id
        if "uniq_id" in kwargs and kwargs["uniq_id"]:
            req_url = self.build_url(self.api_fieldinnerrange, kwargs)
            self.raw_data = self.http_request.get(req_url).read()
        else:
            if "uniq_id" in kwargs:
                del kwargs["uniq_id"]
            req_url = self.build_url(self.api_fieldinnerrange)
            self.raw_data = self.http_request.post(req_url, self.build_post_param(kwargs)).read()

    @dec_log()
    def field_delete(self, tb_id, fd_name="", fid="", query_for_ct=None):
        req_param = {
            "tb_id": tb_id,
            "fid": fid,
            # "field_name": fd_name,
        }

        if query_for_ct is not None:
            req_param["query_for_ct"] = query_for_ct

        req_url = self.build_url(self.api_fielddelete)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def field_create(self, tb_id, field_name, aggreg, data_type, original_field_name="", flag=0, params="",
                     query_for_ct=None, need_param=None):

        real_params = {}
        if isinstance(params, dict):
            real_params = params
        assert isinstance(aggreg, str) or isinstance(aggreg, unicode)

        req_param = {
            "tb_id": tb_id,
            "new_field_name": field_name,
            "aggregator": aggreg,
            "data_type": data_type,
            "original_field_name": original_field_name,
            "flag": flag,
            "param": json.dumps(real_params)
        }

        if query_for_ct is not None:
            req_param["query_for_ct"] = query_for_ct

        if need_param is not None:
            req_param["need_param"] = need_param

        req_url = self.build_url(self.api_fieldcreate)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def field_modify(self, tb_id, field_name, fid, aggreg, data_type, original_field_name="", flag=0, param="", query_for_ct=None):

        real_param = {}
        if isinstance(param, dict):
            real_param = param

        assert isinstance(aggreg, str)
        req_param = {
            "tb_id": tb_id,
            "fid": fid,
            "new_field_name": field_name,
            "aggregator": aggreg,
            "data_type": data_type,
            "original_field_name": original_field_name,
            "flag": flag
        }
        if data_type == "string":
            req_param["param"] = real_param

        if query_for_ct is not None:
            req_param["query_for_ct"] = query_for_ct

        req_url = self.build_url(self.api_fieldmodify)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def field_modify_ex(self, **bags):

        for k, v in bags.iteritems():
            if type(v) in (dict, list):
                bags[k] = json.dumps(v)
            else:
                assert type(v) in (int, str, unicode, float)

        req_url = self.build_url(self.api_fieldmodify)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(bags)).read()

    @dec_log()
    def field_itemsearch(self, tb_id, field, keyword):

        req_param = {
            "tb_id": tb_id,
            "field": json.dumps({
                "type": "dimension",
                "name": field["f_name"],
                "data_type": field.type_str(),
                "editable": True,
                "is_build_aggregated": field.is_build_aggregated(),
                "formula": field["formula"],
                "fid": field["fid"],
                "original_name": field["f_name"],
                "param": field["param"],
                "is_calc_field": True
            }),
            "keyword": keyword

        }
        req_url = self.build_url(self.api_fielditemsearch)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def field_validate(self, tb_id, field, items):

        assert isinstance(items, list)

        req_param = {
            "tb_id": tb_id,
            "field": json.dumps({
                "type": "dimension",
                "name": field["f_name"],
                "data_type": field.type_str(),
                "editable": False,
                "is_build_aggregated": field.is_build_aggregated(),
                "formula": field["formula"],
                "fid": field["fid"],
                "original_name": field["f_name"],
                "param": field["param"],
                "is_calc_field": True
            }),
            "items": json.dumps(items)
        }
        req_url = self.build_url(self.api_fieldvalidate)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def adv_enum_list(self, ct_id, tb_id, fid, search_key):
        req_param = {
            "ct_id": ct_id,
            "tb_id": tb_id,
            "fid": fid,
            "keyword": search_key
        }

        # 机器学习复用这个接口, 不传ct_id
        if ct_id is None:
            del req_param["ct_id"]

        req_url = self.build_url(self.api_enumlist, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    @dec_log()
    def adv_enum_modify(self, ct_id, tb_id, etype, fid, config, layer_id=""):
        req_param = {
            "ct_id": ct_id,
            "tb_id": tb_id,
            "type": etype,
            "fid": fid,
            "config": config
        }

        if layer_id:
            req_param["layer_id"] = layer_id

        req_url = self.build_url(self.api_advenummodify)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def adv_enum_modify_ex(self, ct_id, tb_id, etype, fid, config, range_type, layer_id=""):
        req_param = {
            "ct_id": ct_id,
            "tb_id": tb_id,
            "type": etype,
            "range_type": range_type,
            "fid": fid,
            "config": config
        }

        if layer_id:
            req_param["layer_id"] = layer_id
        req_url = self.build_url(self.api_advenummodify)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def adv_enum_delete(self, ct_id, tb_id, fid):
        req_param = {
            "ct_id": ct_id,
            "tb_id": tb_id,
            "fid": fid
        }
        req_url = self.build_url(self.api_advenumdelete, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    @dec_log()
    def adv_enum_search(self, **kwargs):

        for k, v in kwargs.iteritems():
            if not (isinstance(v, str) or isinstance(v, unicode)):
                kwargs[k] = json.dumps(v)

        req_url = self.build_url(self.api_advenumsearch)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(kwargs)).read()

    @dec_log()
    def adv_num_modify(self, ct_id, tb_id, etype, fid, config, layer_id=""):
        req_param = {
            "ct_id": ct_id,
            "tb_id": tb_id,
            "type": etype,
            "fid": fid,
            "config": config
        }
        if layer_id:
            req_param["layer_id"] = layer_id
        req_url = self.build_url(self.api_advnummodify)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def chart_move(self, ct_id, from_dsh, to_dsh, check="do", dash_meta=None):

        assert isinstance(from_dsh, dict)
        assert isinstance(to_dsh, dict)
        req_param = {
            "ct_id": ct_id,
            "from": json.dumps(from_dsh),
            "to": json.dumps(to_dsh),
            "check": check,
            "dsh_meta": json.dumps(dash_meta),
        }
        req_url = self.build_url(self.api_chartmove, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    @expect_succ
    @dec_log()
    def chart_modify(self, ct_id, data):
        assert isinstance(data, str) or isinstance(data, dict)
        if isinstance(data, dict):
            data = json.dumps(data)
        req_param = {
            "ct_id": ct_id,
            "data": data
        }
        req_url = self.build_url(self.api_chartmodify)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def dsh_filter_item(self, dsh_id, rule_id=''):
        req_param = {
            "dsh_id": dsh_id,
            "rule_id": rule_id
        }
        req_url = self.build_url(self.api_dshfilteritem)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def mob_dsh_filter_item(self, dsh_id, rule_id=''):
        req_param = {
            "dsh_id": dsh_id,
            "rule_id": rule_id
        }
        req_url = self.build_url(self.api_mobdshfilteritem)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def dsh_filter_list(self, dsh_id, rule_id=""):
        req_param = {
            "dsh_id": dsh_id,
            "rule_id": rule_id
        }
        req_url = self.build_url(self.api_dshfilterlist)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def dsh_filter_commit(self, dsh_id, data):

        assert isinstance(data, list)
        req_param = {
            "dsh_id": dsh_id,
            "data": json.dumps(data)
        }
        req_url = self.build_url(self.api_dshfiltercommit)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def dashboard_info(self, atime, dsh_id):
        req_param = {
            "time": atime,
            "dsh_id": dsh_id
        }
        req_url = self.build_url(self.api_dashboardinfo, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    @dec_log()
    def dashboard_filter_range(self, dsh_id, df_id, granularity="", rule_id="", parent_range="", selected_tables=None,
                               scheme_id=""):

        real_parent_range = []
        if isinstance(parent_range, list):
            real_parent_range = parent_range

        req_param = {
            "dsh_id": dsh_id,
            "df_id": df_id,
            "rule_id": rule_id,
            "granularity": granularity,
            "parent_range": json.dumps(real_parent_range),
            "scheme_id": scheme_id
        }
        if selected_tables is not None:
            req_param["selected_tables"] = json.dumps(selected_tables)

        req_url = self.build_url(self.api_dashfilterrange)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def dashboard_filter_enum_search(self, df_id, search_key, rule_id="", granu="", parent_range=""):
        req_param = {
            "df_id": df_id,
            "keyword": search_key,
            "rule_id": rule_id,
        }
        if granu:
            req_param["granularity"] = granu
        if parent_range:
            req_param["parent_range"] = json.dumps(parent_range)

        req_url = self.build_url(self.api_dashfilterenumsearch)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def mob_chart_data(self, ct_id, system, app_ver, test_on, dsh_id=None, linked_chart_type=None, tb_sort="",
                       filter_ops="", drill_ops="", rule_id="", last_cache_time=None, advanced_sort='',
                       display_granularity=None):
        req_param = {
            "ct_id": ct_id,
            "tb_sort": tb_sort,
            "system": system,
            "app_ver": app_ver,
            "test": "1" if test_on else "0"
        }

        # drill options
        real_drill_ops = {}

        if isinstance(drill_ops, dict):
            real_drill_ops = drill_ops

        for a, b in real_drill_ops.items():
            if type(b) in (list, dict):
                req_param[a] = json.dumps(b)
            else:
                req_param[a] = b

        # 有些时候查询是带有过滤器参数的，这里处理一下
        real_filter_ops = {}

        if isinstance(filter_ops, dict):
            real_filter_ops = filter_ops

        for fop, v in real_filter_ops.items():
            req_param[fop] = v if isinstance(v, str) else json.dumps(v)

        # 这里处理排序参数
        if len(tb_sort) == 0:
            req_param.pop("tb_sort")

        if dsh_id:
            req_param["dsh_id"] = dsh_id

        # 模板分配的图表需要rule_id
        if rule_id:
            req_param["rule_id"] = rule_id

        if last_cache_time is not None:
            req_param["last_cache_time"] = last_cache_time

        if advanced_sort:
            req_param["advanced_sort"] = json.dumps(advanced_sort)
            req_param["is_advanced_sort"] = 1

        # 图表日期粒度切换
        if display_granularity:
            assert isinstance(display_granularity, dict)
            req_param["display_granularity"] = json.dumps(display_granularity)

        req_url = self.build_url(self.mobapi_chartdata)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def ds_list(self):
        req_param = {
            "_t": time.time()
        }
        req_url = self.build_url(self.api_dslist, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    @dec_log()
    def ds_delete(self, ds_id):
        req_param = {
            "ds_id": ds_id,
            "_t": time.time(),
        }
        req_url = self.build_url(self.api_dsdelete, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    @dec_log()
    def ds_tblist(self):
        req_param = {
            "_t": time.time(),
        }
        req_url = self.build_url(self.api_dstblist, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    @dec_log()
    def ds_conn_api(self, db_type, username='', password='', token=''):
        if db_type == 6:
            req_param = dict(
                _t=time.time(),
                db_type=db_type,
                token=token,
            )
        else:
            req_param = dict(
                _t=time.time(),
                db_type=db_type,
                username=username,
                password=password,
                token=token,
            )
        # if token:
        #     req_param["token"] = token

        req_url = self.build_url(self.api_dsconn)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def ds_conn_db(self, db_type, username, password, host='', database='', port=''):

        req_param = dict(
            _t=time.time(),
            db_type=db_type,
            username=username,
            password=password,
            host=host,
            database=database,
            port=port,
        )

        req_url = self.build_url(self.api_dsconn)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def ds_cdstb(self, db_type, username, password, host, database, port):

        req_param = dict(
            _t=time.time(),
            db_type=db_type,
            host=host,
            database=database,
            port=port,
            username=username,
            password=password

        )

        req_url = self.build_url(self.api_dscdstb)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def ds_cdstb_api(self, db_type, username, password):

        req_param = dict(
            _t=time.time(),
            db_type=db_type,
            username=username,
            password=password

        )

        req_url = self.build_url(self.api_dscdstb)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def ds_create(self, db_type, **var_params):

        req_param = dict(
            _t=time.time(),
            db_type=db_type,
            is_pause=0,
            hour=00,
            minute=00
        )

        req_param.update(var_params)

        req_param.update({k: (json.dumps(v) if not isinstance(v, str) else v) for k, v in var_params.iteritems()})
        req_url = self.build_url(self.api_dscreate)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def ds_info(self, ds_id):
        req_param = {
            "ds_id": ds_id,
            "_t": time.time(),
        }
        req_url = self.build_url(self.api_dsinfo, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    @dec_log()
    def ds_sheet(self, ds_id):

        req_param = dict(
            _t=time.time(),
            ds_id=ds_id,
        )

        req_url = self.build_url(self.api_dssheet)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def ds_task(self, ds_id):

        req_param = dict(
            _t=time.time(),
            ds_id=ds_id,
        )

        req_url = self.build_url(self.api_dstask)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def ds_sync(self, ds_id):

        req_param = dict(
            _t=time.time(),
            ds_id=ds_id,
        )

        req_url = self.build_url(self.api_dssync)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def ds_syncdb(self, ds_id, new_table):

        req_param = dict(
            _t=time.time(),
            ds_id=ds_id,
            new_table=new_table
        )
        req_url = self.build_url(self.api_dssync, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    @dec_log()
    def api_dsfielddel(self, ds_id, fname, ftitle, fvalue):

        req_param = dict(
            _t=time.time(),
            ds_id=ds_id,
            fname=fname,
            ftitle=ftitle,
            fvalue=fvalue
        )

        req_url = self.build_url(self.api_dsfielddel)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def ds_modify(self, db_type, **kwargs):

        req_param = dict(
            _t=time.time(),
            db_type=db_type
        )
        req_param.update(kwargs)

        req_param.update({k: (json.dumps(v) if not isinstance(v, str) else v) for k, v in kwargs.iteritems()})

        req_url = self.build_url(self.api_dsmodify)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def ds_conn(self, db_type, **var_params):

        req_param = dict(
            _t=time.time(),
            db_type=db_type,
        )

        req_param.update(var_params)

        req_param.update({k: (json.dumps(v) if not isinstance(v, str) else v) for k, v in var_params.iteritems()})

        req_url = self.build_url(self.api_dsconn)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def ds_rename(self, ds_id, name):

        req_param = dict(
            _t=time.time(),
            ds_id=ds_id,
            name=name,
        )

        req_url = self.build_url(self.api_dsrename)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def ds_allot(self, ds_id, name, db_type, user_id_list):

        req_param = dict(
            _t=time.time(),
            ds_id=ds_id,
            name=name,
            db_type=db_type,
            user_id_list=user_id_list,
        )

        req_url = self.build_url(self.api_dsallot)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def ds_oplog(self, **var_params):

        req_param = dict(
            _t=time.time(),
        )

        req_param.update(var_params)
        req_param.update({k: (json.dumps(v) if not isinstance(v, str) else v) for k, v in var_params.iteritems()})
        print req_param
        req_url = self.build_url(self.api_dsoplog)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def enum_order_info(self, fid, tb_id):
        req_param = {
            "fid": fid,
            "tb_id": tb_id
        }
        req_url = self.build_url(self.api_enumorderinfo, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    @dec_log()
    def enum_order_update(self, config_list):
        # 原接口传参为单个字段信息, fid, tb_id, template=None, order_type=1

        assert isinstance(config_list, list)
        for f in config_list:
            assert isinstance(f, dict)
            if "template" in f and f["template"] is None:
                del f["template"]

        req_param = dict(
            config_list=json.dumps(config_list)
        )

        req_url = self.build_url(self.api_enumorderupdate, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    @dec_log()
    def folder_create(self, name, parent_id):
        req_param = {
            "_t": time.time(),
            "name": name,
            "parent_id": parent_id,
        }
        req_url = self.build_url(self.api_foldercreate)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def folder_modifyparent(self, folder_id, parent_id, seq_no=0):
        req_param = dict(
            folder_id=folder_id,
            parent_id=parent_id,
            seq_no=seq_no,
        )
        req_url = self.build_url(self.api_foldermodifyparent)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def folder_modify(self, folder_id, name):
        req_param = dict(
            folder_id=folder_id,
            name=name,
            _t=time.time(),
        )
        req_url = self.build_url(self.api_foldermodify)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def folder_modifyseq(self, folder_id, seq=0):
        req_param = dict(
            folder_id=folder_id,
            seq=seq,
            _t=time.time(),
        )
        req_url = self.build_url(self.api_foldermodifyseq)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def field_groupexpr_verify(self, tb_id, fid, expression):
        assert isinstance(expression, str)
        req_param = {
            "fid": fid,
            "tb_id": tb_id,
            "expression": expression,
        }
        req_url = self.build_url(self.api_fieldgroupexprverify)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def dash_delete(self, dsh_id):
        req_param = {
            "dsh_id": dsh_id
        }
        req_url = self.build_url(self.api_dashdelete)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def adv_date_delete(self, df_id="", opt_id=""):

        req_param = {
            "opt_id": opt_id,
        }
        if df_id:
            req_param["df_id"] = df_id

        req_url = self.build_url(self.api_advdatedel)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def table_copy(self, original_name, new_name, tb_id, folder_id="folder_root"):

        req_param = dict(
            original_tb_name=original_name,
            tb_name=new_name,
            tb_id=tb_id,
            folder_id=folder_id
        )

        req_url = self.build_url(self.api_tablecopy)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def model_struct(self, tb_id):

        req_param = dict(
            tb_id=tb_id,
        )

        req_url = self.build_url(self.api_modelstruct)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def partition_set(self, tb_id, fid, ftype, opt):

        req_param = dict(
            tb_id=tb_id,
            base_field=fid,
            param=json.dumps(dict(
                type=ftype,
                option=opt
            )),
        )

        req_url = self.build_url(self.api_partset)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def partition_remove(self, tb_id):

        req_param = dict(
            tb_id=tb_id,
        )

        req_url = self.build_url(self.api_partrm)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def dashboard_copy(self, old_dsh_id, to_proj_id, new_dsh_name, ws_id=""):

        req_param = dict(
            dsh_id=old_dsh_id,
            to_proj_id=to_proj_id,
            dsh_name=new_dsh_name,
            ws_id=ws_id,
        )

        req_url = self.build_url(self.api_dashcopy)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def field_selected_modify(self, tb_id, field_ids):
        assert isinstance(field_ids, list)

        req_param = dict(
            tb_id=tb_id,
            field_ids=json.dumps(field_ids),
        )

        req_url = self.build_url(self.api_fieldselectedmodify)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def field_enum_filter(self, tb_id, field_id, filter_str, limit):

        req_param = dict(
            tb_id=tb_id,
            field_id=field_id,
            filter_str=filter_str,
            limit=limit
        )

        req_url = self.build_url(self.api_fieldenumfilter)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def check_field_dependency(self, tb_id, del_field_titles):
        assert isinstance(del_field_titles, list)

        req_param = {
            "tb_id": tb_id,
            "del_field_titles": json.dumps(del_field_titles)
        }

        req_url = self.build_url(self.api_checkfielddepend)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def excel_replace_one(self, excel_id, tb_id, sheet_name, title_mapping, add_fields, del_fields, map_id):
        assert isinstance(title_mapping, dict)
        assert isinstance(add_fields, list)
        assert isinstance(del_fields, list)

        req_param = {
            "excel_id": excel_id,
            "tb_id": tb_id,
            "sheet_name": sheet_name,
            "tb_title_ex_title_mapping": json.dumps(title_mapping),
            "add_field_titles": json.dumps(add_fields),
            "del_field_titles": json.dumps(del_fields),
            "map_id": map_id,
            "force": "1",
        }

        req_url = self.build_url(self.api_excelreplaceone, req_param)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    def enumcolor_fieldrange(self, ct_id, tb_id, field_info):

        req_param = dict(
            tb_id=tb_id,
            ct_id=ct_id,
            field=json.dumps(field_info),
        )

        req_url = self.build_url(self.api_enumcolorfieldrange)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def excel_append_batch(self, tb_id, excel_file):

        if hasattr(excel_file, "read"):
            filename = excel_file.filename
            fp = excel_file
        else:
            filename = os.path.basename(excel_file)
            fp = open(excel_file)

        boundary = ''.join(random.sample('abcdefgABCDEFG1234567', 16))

        print tb_id
        data = list()
        data.append("--%s" % boundary)
        data.append('Content-Disposition: form-data; name="opt"\r\n')
        data.append('1')
        data.append("--%s" % boundary)
        data.append('Content-Disposition: form-data; name="folder_id"\r\n')
        data.append('folder_root')
        data.append("--%s" % boundary)
        data.append('Content-Disposition: form-data; name="tb_id"\r\n')
        data.append(str(tb_id))
        data.append("--%s" % boundary)
        data.append('Content-Disposition: form-data; name="file"; filename="%s"' % filename)
        data.append('Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet\r\n')

        data.append(fp.read())
        fp.close()

        data.append("--%s--\r\n" % boundary)

        self.raw_data = self.http_request.post(
            self.build_url(BdpSDK.api_excelappendbatch),
            '\r\n'.join(data),
            headers={"Content-Type": 'multipart/form-data; boundary=%s' % boundary}
        ).read()

    def excel_title_check(self, titles):

        assert isinstance(titles, list)
        req_param = dict(
            titles=json.dumps(titles),
        )

        req_url = self.build_url(self.api_exceltitlecheck)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    def chart_size_groups(self, ct_id, bubble_setting):

        req_param = dict(
            ct_id=ct_id,
            bubble_setting=json.dumps(bubble_setting),
        )

        req_url = self.build_url(self.api_chartsizegroups)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    def transfer_gis_field(self, tb_id, field_id):

        req_param = dict(
            tb_id=tb_id,
            field_id=field_id,
        )

        req_url = self.build_url(self.api_gistransfer)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def update_mode_modify(self, tb_id, mode, fid="", ftype="", opt=""):

        if fid == "":
            req_param = dict(
                _t=time.time(),
                tb_id=tb_id,
                mode=mode,
            )

        else:
            req_param = dict(
                _t=time.time(),
                tb_id=tb_id,
                mode=mode,
                param=json.dumps(dict(
                    base_field=fid,
                    param=json.dumps(dict(
                        type=ftype,
                        option=opt
                    ))
                )),
            )

        req_url = self.build_url(self.api_tbupdate_mode_modify)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def update_mode_check(self, tb_id, mode):

        req_param = dict(
            _t=time.time(),
            tb_id=tb_id,
            mode=mode,
        )

        req_url = self.build_url(self.api_tbupdate_mode_check)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    def chart_link_info(self, ct_id):

        req_param = dict(
            ct_id=ct_id,
        )

        req_url = self.build_url(self.api_chartlinkinfo)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    def chart_link_commit(self, ct_id, link_info):

        req_param = dict(
            ct_id=ct_id,
            link_info=link_info
        )

        req_url = self.build_url(self.api_chartlinkcommit)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    def chart_link_delete(self, ct_id):

        req_param = dict(
            ct_id=ct_id,
        )

        req_url = self.build_url(self.api_chartlinkdelete)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def warn_add(self, ct_id, data, rule_id=""):

        req_param = dict(
            _t=time.time(),
            ct_id=ct_id,
            data=json.dumps(data),
            rule_id=rule_id,
        )

        req_url = self.build_url(self.api_warnadd, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    @dec_log()
    def warn_switch(self, ct_id, off_warn_ids, open_warn_ids, rule_id=""):

        req_param = dict(
            _t=time.time(),
            ct_id=ct_id,
            off_warn_ids=json.dumps(off_warn_ids),
            open_warn_ids=json.dumps(open_warn_ids),
            rule_id=rule_id,
        )

        req_url = self.build_url(self.api_warnswitch, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    @dec_log()
    def warn_modify(self, ct_id, warn_id, data, rule_id=""):

        req_param = dict(
            _t=time.time(),
            ct_id=ct_id,
            data=json.dumps(data),
            rule_id=rule_id,
            warn_id=warn_id,
        )

        req_url = self.build_url(self.api_warnmodify, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    @dec_log()
    def warn_delete(self, ct_id, warn_id, rule_id=""):

        req_param = dict(
            _t=time.time(),
            ct_id=ct_id,
            rule_id=rule_id,
            warn_id=warn_id,
        )

        req_url = self.build_url(self.api_warndelete, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    @dec_log()
    def tb_editable_schema(self, tb_id):
        req_param = {
            "_t": time.time(),
            "tb_id": tb_id
        }
        req_url = self.build_url(self.api_tbeditable_schema, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    @dec_log()
    def _dsh_order(self, proj_id, dsh_sort=[], proj_type=0):

        req_param = dict(
            _t=time.time(),
            proj_id=proj_id,
            type=proj_type,
            sort=json.dumps(dsh_sort),
        )

        req_url = self.build_url(self.api_dshorder)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def dsh_move(self, dsh_id, proj_id, dsh_sort=[], proj_type=0):

        req_param = dict(
            _t=time.time(),
            dsh_id=dsh_id,
            parent_id=proj_id,
            type=proj_type,
            sort=json.dumps(dsh_sort),
        )
        req_url = self.build_url(self.api_dshmove)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def folder_batch_change(self, move_tbs, folder_id):
        assert isinstance(move_tbs, list)

        req_param = dict(
            _t=time.time(),
            change_folders=json.dumps(move_tbs),
            to_folder=folder_id,
        )

        req_url = self.build_url(self.api_folderbatchchange)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def sql_format(self, sql):

        req_param = dict(
            _t=time.time(),
            sql=sql,
        )

        req_url = self.build_url(self.api_sqlformat)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    def table_sharelist(self, tb_id):
        req_param = {
            "_t": time.time(),
            "tb_id": tb_id
        }
        req_url = self.build_url(self.api_share_alllist, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    @dec_log()
    def tb_share_modify(self, tb_id, user_all, user_del, group_all, group_del):
        req_param = {
            "_t": time.time(),
            "tb_id": tb_id,
            "user_list": json.dumps({
                "all": user_all,
                "del": user_del,
            }),
            "group_list": json.dumps({
                "all": group_all,
                "del": group_del,
            }),
        }

        req_url = self.build_url(self.api_share_modify)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def tb_modify_tag(self, data):

        assert isinstance(data, list)

        req_param = dict(
            data=json.dumps(data),
        )

        req_url = self.build_url(self.api_tbmodifytag)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def excel_download(self, ex_id, tb_id):
        req_param = {
            "_t": time.time(),
            "excel_id": ex_id,
            "tb_id": tb_id
        }
        req_url = self.build_url(self.api_exceldownload, req_param)
        raw_resp = self.http_request.get(req_url)

        content_len = int(raw_resp.headers["Content-Length"])
        content_disp = raw_resp.headers["Content-Disposition"]
        content_dict = {}
        for i in content_disp.split(';'):
            try:
                k, v = i.split('=')
                if k.strip() == "filename":
                    break
            except:
                k, v = "", ""

        if k:
            content_dict[k.strip()] = v.strip().strip('"')

        local_file = content_dict["filename"]

        filename = bdpconf.DOWNLOAD_DIR + "/" + local_file

        if os.path.exists(filename):
            os.remove(filename)

        fp = open(filename, "wb")

        for i in raw_resp.iter_content(chunk_size=4096):
            fp.write(i)

        assert fp.tell() == content_len

        fp.close()

    def current_tb(self, tb_id):
        req_param = {
            "_t": time.time(),
            "tb_id": tb_id
        }
        req_url = self.build_url(self.api_currenttb, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    def all_folder_name(self):
        req_param = {
            "_t": time.time()
        }
        req_url = self.build_url(self.api_allfoldername, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    def folder_tb_list(self, folder_id):
        req_param = {
            "_t": time.time(),
            "folder_id": folder_id
        }
        req_url = self.build_url(self.api_foldercontaintb, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    def tb_capacity_list(self, page=0, sub_id="", keyword="", show_all=0):
        req_param = {
            "_t": time.time(),
            "page": page,
            "sub_id": sub_id,
            "keyword": keyword,
            "show_all": show_all
        }
        req_url = self.build_url(self.api_tbcapacity, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    def tb_stat_group(self):
        req_param = {
            "_t": time.time(),
        }
        req_url = self.build_url(self.api_tbstatgroup, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    @dec_log()
    def tb_replace_check(self, join_tb_id, src_tb_id, target_tb_id, target_tb_key=""):
        req_param = {
            "_t": time.time(),
            "join_tb_id": join_tb_id,
            "src_tb_id": src_tb_id,
            "target_tb_id": target_tb_id,
        }

        if target_tb_key:
            req_param["target_tb_key"] = target_tb_key

        req_url = self.build_url(self.api_wbreplace_check)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def chart_delrelatb(self, ct_id, tb_id):

        req_param = dict(
            ct_id=ct_id,
            tb_id=tb_id,
        )

        req_url = self.build_url(self.api_chartdelrelatb)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def chart_addrelatb(self, ct_id, tb_id):

        req_param = dict(
            ct_id=ct_id,
            tb_id=tb_id,
        )

        req_url = self.build_url(self.api_chartaddrelatb)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def tb_relalist(self, tb_id):
        req_param = dict(
            tb_id=tb_id,
        )

        req_url = self.build_url(self.api_tbrelalist)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def chart_copy(self, ct_id, from_dict, to_dict):
        req_param = {
            "ct_id": ct_id,
            "from": json.dumps(from_dict),
            "to": json.dumps(to_dict),
        }

        req_url = self.build_url(self.api_chartcopy)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def chart_modify_tb(self, ct_id, tb_id):
        req_param = {
            "ct_id": ct_id,
            "tb_id": tb_id,
        }

        req_url = self.build_url(self.api_chartmodify_tb)

        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def table_batch_delete(self, tb_list):
        req_param = {
            "_t": time.time(),
            "tb_list": json.dumps(tb_list),
            "session_id": '',
            "verify_code": '',
        }

        req_url = self.build_url(self.api_tbbatchdelete)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def table_check_rely(self, tb_list):
        req_param = {
            "_t": time.time(),
            "tb_list": json.dumps(tb_list)
        }

        req_url = self.build_url(self.api_tbcheckrely)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def folder_filter(self, filter_str):
        req_param = {
            "_t": time.time(),
            "filter_str": filter_str
        }

        req_url = self.build_url(self.api_folderfilter, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    def wb_export(self, info):
        boundary = ''.join(random.sample('abcdefgABCDEFG1234567', 16))

        data = list()
        data.append("--%s" % boundary)
        data.append('Content-Disposition: form-data; name="info"\r\n')
        data.append(json.dumps(info))
        data.append("--%s--\r\n" % boundary)

        raw_resp = self.http_request.post(self.build_url(BdpSDK.api_wb_export),
                                          '\r\n'.join(data),
                                          headers={"Content-Type": 'multipart/form-data; boundary=%s' % boundary})

        content_disp = raw_resp.headers["Content-Disposition"]
        content_len = int(raw_resp.headers["Content-Length"])

        content_dict = {}
        for i in content_disp.split(';'):
            try:
                k, v = i.split('=')
            except:
                k, v = "", ""

            if k:
                content_dict[k.strip()] = v.strip().strip('"')

        local_file = content_dict["filename"]

        filename = bdpconf.DOWNLOAD_DIR + "/" + local_file

        if os.path.exists(filename):
            os.remove(filename)

        fp = open(filename, "wb")

        for i in raw_resp.iter_content(chunk_size=4096):
            fp.write(i)

        assert fp.tell() == content_len

        fp.close()

    def enum_order_filter_info(self, tb_id, fid, ct_id, drill_level='0', index='0', axis='x'):
        req_param = {
            "tb_id": tb_id,
            "fid": fid,
            "ct_id": ct_id,
            "drill_level": drill_level,
            "index": index,
            "axis": axis
        }
        req_url = self.build_url(self.api_enum_orderfilter_info, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    @dec_log()
    def table_share_info(self, tb_id):
        req_param = {
            "_t": time.time(),
            "tb_id": tb_id
        }

        req_url = self.build_url(self.api_tb_shareinfo)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def user_modify_info(self, contact, sex, position):
        req_param = {
            "_t": time.time(),
            "contact": contact,
            "sex": sex,
            "position": position,
        }

        req_url = self.build_url(self.api_usermodifyinfo)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def chart_filter_cmp_date_range(self, date_filter="", yoyqoqsetting=""):

        req_param = {
            "date_filter": json.dumps({} if not date_filter else date_filter),
            "yoyQoqSetting": json.dumps({} if not yoyqoqsetting else yoyqoqsetting),
        }

        req_url = self.build_url(self.api_chartfiltercmpdaterange)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def get_field_length(self, tb_id, data_type, aggregator="", param={}):
        req_param = {
            "_t": time.time(),
            "tb_id": tb_id,
            "aggregator": aggregator,
            "data_type": data_type,
            "param": json.dumps(param)
        }

        req_url = self.build_url(self.api_fieldlength)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def adv_date_scheme_create(self, name):
        req_param = {
            "_t": time.time(),
            "name": name,
        }

        req_url = self.build_url(self.api_adv_date_scheme_create)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def adv_date_scheme_delete(self, scheme_id):
        req_param = {
            "_t": time.time(),
            "scheme_id": scheme_id,
        }

        req_url = self.build_url(self.api_adv_date_scheme_delete)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def adv_date_scheme_modify(self, name, scheme_id):
        req_param = {
            "_t": time.time(),
            "name": name,
            "scheme_id": scheme_id,
        }

        req_url = self.build_url(self.api_adv_date_scheme_modify)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def adv_date_scheme_list(self):
        req_param = {
            "_t": time.time(),
        }

        req_url = self.build_url(self.api_adv_date_scheme_list)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def param_range(self, tb_id, fid, range_type):
        req_param = {
            "tb_id": tb_id,
            "field_id": fid,
            "range_type": range_type
        }

        req_url = self.build_url(self.api_paramrange, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    @dec_log()
    def param_create(self, tb_id, name, type, config, default_value="", comment=""):
        req_param = {
            "tb_id": tb_id,
            "name": name,
            "type": type,
            "config": json.dumps(config),
            "param_id": "",
            "default_value": default_value,
            "comment": comment,
        }
        req_url = self.build_url(self.api_paramcreate)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def param_list(self, tb_id):
        req_param = {
            "tb_id": tb_id
        }

        req_url = self.build_url(self.api_paramlist)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def param_delete(self, tb_id, param_id):
        req_param = {
            "tb_id": tb_id,
            "param_id": param_id
        }

        req_url = self.build_url(self.api_paramdelete)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    @dec_log()
    def param_modify(self, tb_id, param_id, name, type, config, default_value="", comment=""):
        req_param = {
            "tb_id": tb_id,
            "param_id": param_id,
            "name": name,
            "type": type,
            "config": json.dumps(config),
            "default_value": default_value,
            "comment": comment
        }

        req_url = self.build_url(self.api_parammodify)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()

    def ds_nslist(self, db_type, keyword):
        req_param = {
            "_t": time.time(),
            "db_type": db_type,
            "keyword": keyword,
            "order_by": 1,
            "page": 1,
            "status_type": 0
        }

        req_url = self.build_url(self.api_nslist, req_param)
        self.raw_data = self.http_request.get(req_url).read()

    @dec_log()
    def ds_usersync(self, ds_id, db_type, name, start_date):
        req_param = {
            "_t": time.time(),
            "ds_id": ds_id,
            "db_type": db_type,
            "name": name,
            "start_date": start_date,
        }

        req_url = self.build_url(self.api_usersync)
        self.raw_data = self.http_request.post(req_url, self.build_post_param(req_param)).read()
