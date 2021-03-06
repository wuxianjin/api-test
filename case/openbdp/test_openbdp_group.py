#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ = '5xianjin'
import json
from lib.openbdp_sdk import OpenbdpSdk
import pytest
import time
import random


class TestOpenbdpGroupCase:
    # 随机生成手机号码
    def createPhone(self):
        prelist = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152",
                   "153", "155", "156", "157", "158", "159", "186", "187", "188"]
        return random.choice(prelist) + "".join(random.choice("0123456789") for i in range(8))

    # 只限超管调用
    def test_openbdp_group_update_fields(self):
        openbdp = OpenbdpSdk.instance()
        # 配置分组自定义字段
        data = [
            {
                "name": "密级",
                "type": "text",
                "config": {
                    "hint": "Please input..."
                }
            },

            {
                "name": "手机品牌",
                "type": "select",
                "config": {
                    "options": ["apple", "vivo", "huawei"]
                }
            }
        ]

        openbdp.call_method_and_succ("openbdp_group_update_fields", data)
        res = openbdp.call_method_and_succ("openbdp_group_list_fields", ret_expr='["result"]')
        # print sorted(res)
        assert sorted(res)[0]['name'] == "密级"
        assert sorted(res)[0]['type'] == "text"
        assert sorted(res)[1]['name'] == "手机品牌"
        assert sorted(res)[1]['type'] == "select"



    def test_openbdp_groupcreate(self):
        openbdp = OpenbdpSdk.instance()
        name = "groupname" + str(time.time())
        pid = openbdp.call_method_and_succ("openbdp_grouplist", ret_expr='["result"][0]["group_id"]')
        gid = openbdp.call_method_and_succ("openbdp_groupcreate", name, pid, ret_expr='["result"]')
        result = openbdp.call_method_and_succ("openbdp_groupinfo", gid, ret_expr='["result"]')
        assert result["name"] == name
        assert result["group_id"] == gid
        assert result["parent_id"] == pid
        # 清除测试数据
        resp = openbdp.call_method_and_succ("openbdp_groupdel", gid, ret_expr='')
        assert resp["status"] == "0"

    def test_openbdp_groupmodify(self):
        openbdp = OpenbdpSdk.instance()
        name = "groupname" + str(time.time())
        pid = openbdp.call_method_and_succ("openbdp_grouplist", ret_expr='["result"][0]["group_id"]')
        count = 0
        while (count < 2):
            gid = openbdp.call_method_and_succ("openbdp_groupcreate", name, pid, ret_expr='["result"]')
            if count == 0:
                T = gid
            result = openbdp.call_method_and_succ("openbdp_groupinfo", gid, ret_expr='["result"]')
            assert result["name"] == name
            assert result["group_id"] == gid
            assert result["parent_id"] == pid
            count = count + 1
            name = "1groupname" + str(time.time())
        # # 修改分组1
        name1 = "openbdpmodifygroupname" + str(time.time())
        resp = openbdp.call_method_and_succ("openbdp_groupmodify", gid, name1, T, ret_expr='')
        assert resp["status"] == "0"
        result = openbdp.call_method_and_succ("openbdp_groupinfo", gid, ret_expr='["result"]')
        assert result["name"] == name1
        assert result["group_id"] == gid
        assert result["parent_id"] == T
        # #清除测试数据
        resp = openbdp.call_method_and_succ("openbdp_groupdel", T, ret_expr='')
        assert resp["status"] == "0"

    def test_openbdp_group_10create(self):
        openbdp = OpenbdpSdk.instance()
        name = "openbdpwuxianjino"
        pid = openbdp.call_method_and_succ("openbdp_grouplist", ret_expr='["result"][0]["group_id"]')
        gid = openbdp.call_method_and_succ("openbdp_groupcreate", name, pid, ret_expr='["result"]')
        T = gid
        result = openbdp.call_method_and_succ("openbdp_groupinfo", gid, ret_expr='["result"]')
        assert result["name"] == name
        assert result["group_id"] == gid
        count = 1
        while (count < 11):
            name = "obwuxianjin" + str(count)
            if count == 10:
                with pytest.raises(AssertionError):
                    openbdp.call_method_and_succ("openbdp_groupcreate", name, gid, ret_expr='["result"]')
                assert json.loads(openbdp.raw_data)["status"] == "12012"
            else:
                ggid = openbdp.call_method_and_succ("openbdp_groupcreate", name, gid, ret_expr='["result"]')
                result = openbdp.call_method_and_succ("openbdp_groupinfo", ggid, ret_expr='["result"]')
                assert result["name"] == name
                assert result["group_id"] == ggid
                gid = ggid
            count = count + 1
        # 清除测试数据
        resp = openbdp.call_method_and_succ("openbdp_groupdel", T, ret_expr='')
        assert resp["status"] == "0"

    def test_openbdp_noparen_id_name(self):
        openbdp = OpenbdpSdk.instance()
        name = ""
        name1 = "1"
        pid = ""
        pid1 = "1"
        with pytest.raises(AssertionError):
            openbdp.call_method_and_succ("openbdp_groupcreate", name, pid1, ret_expr='')
        assert json.loads(openbdp.raw_data)["status"] == "11"
        # todo  业务改动已经修改为pid可以为空
        # with pytest.raises(AssertionError):
        #     openbdp.call_method_and_succ("openbdp_groupcreate", name1, pid, ret_expr='')
        # assert json.loads(openbdp.raw_data)["status"] == "11"

    def test_openbdp_groupname_repeat(self):
        openbdp = OpenbdpSdk.instance()
        name = "groupname" + str(time.time())
        pid = openbdp.call_method_and_succ("openbdp_grouplist", ret_expr='["result"][0]["group_id"]')
        gid = openbdp.call_method_and_succ("openbdp_groupcreate", name, pid, ret_expr='["result"]')
        result = openbdp.call_method_and_succ("openbdp_groupinfo", gid, ret_expr='["result"]')
        assert result["name"] == name
        with pytest.raises(AssertionError):
            openbdp.call_method_and_succ("openbdp_groupcreate", name, pid, ret_expr='')
        assert json.loads(openbdp.raw_data)["status"] == "12002"
        # 清除测试数据
        resp = openbdp.call_method_and_succ("openbdp_groupdel", gid, ret_expr='')
        assert resp["status"] == "0"

    def test_openbdp_group_user_manager(self):
        openbdp = OpenbdpSdk.instance()
        gname = "groupname" + str(time.time())
        pid = openbdp.call_method_and_succ("openbdp_grouplist", ret_expr='["result"][0]["group_id"]')
        gid = openbdp.call_method_and_succ("openbdp_groupcreate", gname, pid, ret_expr='["result"]')
        result = openbdp.call_method_and_succ("openbdp_groupinfo", gid, ret_expr='["result"]')
        assert result["name"] == gname
        assert result["group_id"] == gid
        assert result["parent_id"] == pid
        # add user
        username = "username" + str(time.time())
        name = "name" + str(time.time())
        mobile = self.createPhone()
        password = "123qweasd",
        role = 3
        uid = openbdp.call_method_and_succ("openbdp_userCreate", username, name, mobile, password, role,
                                           ret_expr='["result"]')
        result = openbdp.call_method_and_succ("openbdp_userInfo", uid, ret_expr='["result"]')
        assert result["username"] == username
        assert result["name"] == name
        assert result["mobile"] == mobile
        assert result["role"] == role
        user_ids = [uid]
        # 添加组员
        openbdp.call_method_and_succ("openbdp_group_adduser", gid, user_ids, ret_expr='["result"]')
        result = openbdp.call_method_and_succ("openbdp_groupinfo", gid, ret_expr='["result"]')
        assert result["name"] == gname
        assert result["group_users"][0]["user_id"] == uid
        # 删除组员
        resp = openbdp.call_method_and_succ("openbdp_group_deluser", gid, user_ids, ret_expr='')
        assert resp["status"] == "0"
        result = openbdp.call_method_and_succ("openbdp_groupinfo", gid, ret_expr='["result"]')
        assert result["name"] == gname
        assert len(result["group_users"]) == 0
        # 添加管理员
        openbdp.call_method_and_succ("openbdp_group_addmanager", gid, user_ids, ret_expr='["result"]')
        result = openbdp.call_method_and_succ("openbdp_groupinfo", gid, ret_expr='["result"]')
        assert result["name"] == gname
        assert result["group_managers"][0]["user_id"] == uid
        # 删除管理员
        resp = openbdp.call_method_and_succ("openbdp_group_delmanager", gid, user_ids, ret_expr='')
        assert resp["status"] == "0"
        result = openbdp.call_method_and_succ("openbdp_groupinfo", gid, ret_expr='["result"]')
        assert result["name"] == gname
        assert len(result["group_managers"]) == 0
        # 清除测试数据
        resp = openbdp.call_method_and_succ("openbdp_groupdel", gid, ret_expr='')
        assert resp["status"] == "0"
        resp = openbdp.call_method_and_succ("openbdp_userdelete", uid, ret_expr='')
        assert resp["status"] == "0"




    # 个用户每天调用该类型接口不超过1000次（暂定）
    def quuutest_openbdp_chartdata(self):
        openbdp = OpenbdpSdk.instance()
        ct_id = "ct_f1388840b892b2929a23370ebcd77121"
        count = 0
        while (count < 10001):
            if count == 1000:
                with pytest.raises(AssertionError):
                    result = openbdp.call_method_and_succ("openbdp_chart_data", ct_id, ret_expr='')
                assert json.loads(openbdp.raw_data)["status"] == "140001"
            else:
                openbdp.call_method_and_succ("openbdp_chart_data", ct_id, ret_expr='')
            count = count + 1

