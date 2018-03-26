#!/usr/bin/python
# -*- coding: utf8 -*-
# __author__ = '5xianjin'
import json
from lib.openbdp_sdk import OpenbdpSdk
import pytest
import time
import random


class TestOpenbdpUserCase:
    # 随机生成手机号码
    def createPhone(self):
        prelist = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152",
                   "153", "155", "156", "157", "158", "159", "186", "187", "188"]
        return random.choice(prelist) + "".join(random.choice("0123456789") for i in range(8))

    def test_userfreeze(self):
        openbdp = OpenbdpSdk.instance()
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
        # 冻结
        resp = openbdp.call_method_and_succ("openbdp_userfreeze", uid, ret_expr='')
        assert resp["status"] == "0"
        resp = openbdp.call_method_and_succ("openbdp_userunfreeze", uid, ret_expr='')
        assert resp["status"] == "0"
        # delete
        resp = openbdp.call_method_and_succ("openbdp_userdelete", uid, ret_expr='')
        assert resp["status"] == "0"

    def test_reset_password(self):
        openbdp = OpenbdpSdk.instance()
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
        # 冻结
        resp = openbdp.call_method_and_succ("openbdp_reset_password", uid, ret_expr='')
        assert resp["status"] == "0"
        # delete
        resp = openbdp.call_method_and_succ("openbdp_userdelete", uid, ret_expr='')
        assert resp["status"] == "0"

    def test_errchar(self):
        openbdp = OpenbdpSdk.instance()
        username = "{!;"
        name = "name" + str(time.time())
        mobile = "1"
        password = "123qweasd",
        role = 3
        with pytest.raises(AssertionError):
            result = openbdp.call_method_and_succ("openbdp_userCreate", username, name, mobile, password, role,
                                                  ret_expr='')
        assert json.loads(openbdp.raw_data)["status"] == "1016"
        # assert json.loads(openbdp.raw_data)["errstr"] == "username contains invalid char"

    def test_already_have_username(self):
        openbdp = OpenbdpSdk.instance()
        username = "admin"
        name = "name" + str(time.time())
        mobile = "1"
        password = "123qweasd",
        role = 3
        with pytest.raises(AssertionError):
            result = openbdp.call_method_and_succ("openbdp_userCreate", username, name, mobile, password, role,
                                                  ret_expr='')
        assert json.loads(openbdp.raw_data)["status"] == "8003"

    def test_userlist(self):
        openbdp = OpenbdpSdk.instance()
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
        offset = 0
        limit = 5
        result = openbdp.call_method_and_succ("openbdp_userlist", offset, limit, ret_expr='["result"]')
        assert len(result) >= 1
        # delete
        resp = openbdp.call_method_and_succ("openbdp_userdelete", uid, ret_expr='')
        assert resp["status"] == "0"

    def test_already_have_Phone_email(self):
        openbdp = OpenbdpSdk.instance()
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

        username = "username" + str(time.time())
        with pytest.raises(AssertionError):
            result = openbdp.call_method_and_succ("openbdp_userCreate", username, name, mobile, password, role,
                                                  ret_expr='')
        assert json.loads(openbdp.raw_data)["status"] == "1023"
        # delete
        resp = openbdp.call_method_and_succ("openbdp_userdelete", uid, ret_expr='')
        assert resp["status"] == "0"

    def test_nousername(self):
        openbdp = OpenbdpSdk.instance()
        username = ""
        name = "name" + str(time.time())
        mobile = "1"
        password = "123qweasd",
        # 2:管理员，3:普通账号 | int | 必填 |
        role = 3
        with pytest.raises(AssertionError):
            result = openbdp.call_method_and_succ("openbdp_userCreate", username, name, mobile, password, role,
                                                  ret_expr='')
        assert json.loads(openbdp.raw_data)["status"] == "11"
        # assert json.loads(openbdp.raw_data)["errstr"] == "argument username is missing"

    def test_noname(self):
        openbdp = OpenbdpSdk.instance()
        username = "username" + str(time.time())
        name = ""
        mobile = "1"
        password = "123qweasd",
        # 2:管理员，3:普通账号 | int | 必填 |
        role = 3
        with pytest.raises(AssertionError):
            result = openbdp.call_method_and_succ("openbdp_userCreate", username, name, mobile, password, role,
                                                  ret_expr='')
        assert json.loads(openbdp.raw_data)["status"] == "11"
        # assert json.loads(openbdp.raw_data)["errstr"] == "argument name is missing"

    def test_nomobile(self):
        openbdp = OpenbdpSdk.instance()
        username = "username" + str(time.time())
        name = "1"
        mobile = ""
        password = "123qweasd",
        # 2:管理员，3:普通账号 | int | 必填 |
        role = 3
        with pytest.raises(AssertionError):
            result = openbdp.call_method_and_succ("openbdp_userCreate", username, name, mobile, password, role,
                                                  ret_expr='')
        assert json.loads(openbdp.raw_data)["status"] == "23"
        # assert json.loads(openbdp.raw_data)["errstr"] == "argument mobile is missing"

    def test_nopassword(self):
        openbdp = OpenbdpSdk.instance()
        username = "username" + str(time.time())
        name = "1"
        mobile = "999"
        password = ""
        # 2:管理员，3:普通账号 | int | 必填 |
        role = 3
        with pytest.raises(AssertionError):
            result = openbdp.call_method_and_succ("openbdp_userCreate", username, name, mobile, password, role,
                                                  ret_expr='')
        assert json.loads(openbdp.raw_data)["status"] == "11"
        # assert json.loads(openbdp.raw_data)["errstr"] == "argument password is missing"

    def test_norole(self):
        openbdp = OpenbdpSdk.instance()
        username = "username" + str(time.time())
        name = "1"
        mobile = "1"
        password = "",
        role = ""
        with pytest.raises(AssertionError):
            result = openbdp.call_method_and_succ("openbdp_userCreate", username, name, mobile, password, role,
                                                  ret_expr='')
        assert json.loads(openbdp.raw_data)["status"] == "11"
        # assert json.loads(openbdp.raw_data)["errstr"] == "argument role is missing"

    def test_nomanage_groups(self):
        openbdp = OpenbdpSdk.instance()
        username = "username" + str(time.time())
        name = "1"
        mobile = "1"
        password = "",
        # 2:管理员，3:普通账号 | int | 必填 |
        role = 2
        with pytest.raises(AssertionError):
            result = openbdp.call_method_and_succ("openbdp_userCreate", username, name, mobile, password, role,
                                                  ret_expr='')
        assert json.loads(openbdp.raw_data)["status"] == "11"

    def test_nouser(self):
        openbdp = OpenbdpSdk.instance()
        with pytest.raises(AssertionError):
            openbdp.call_method_and_succ("openbdp_userInfo", "9yyy", ret_expr='')
        assert json.loads(openbdp.raw_data)["status"] == "1009"

    def test_openbdp_userCreate(self):
        openbdp = OpenbdpSdk.instance()
        username = "username" + str(time.time())
        gname = "openbdp" + str(time.time())
        name = "name" + str(time.time())
        mobile = self.createPhone()
        password = "123qweasd",
        email = mobile + "@qq.com"
        # 2:管理员，3:普通账号 | int | 必填 |
        role = 3
        position = "position"
        # 分组数据准备
        pid = openbdp.call_method_and_succ("openbdp_grouplist", ret_expr='["result"][0]["group_id"]')
        count = 0
        while (count < 2):
            gid = openbdp.call_method_and_succ("openbdp_groupcreate", gname, pid, ret_expr='["result"]')
            if count == 0:
                T = gid
            result = openbdp.call_method_and_succ("openbdp_groupinfo", gid, ret_expr='["result"]')
            assert result["name"] == gname
            assert result["group_id"] == gid
            assert result["parent_id"] == pid
            count = count + 1
            gname = "openbdp1groupname" + str(time.time())

        belong_groups = [gid, T]
        openbdp.openbdp_userCreate(username, name, mobile, password, role, email=email, position=position,
                                   belong_groups=belong_groups, has_dsh_permission=1, has_tb_permission=1,
                                   has_data_permission=1, has_dsh_manage_permission=1, has_date_filter_permission=1)
        uid = json.loads(openbdp.raw_data)["result"]
        result = openbdp.call_method_and_succ("openbdp_userInfo", uid, ret_expr='["result"]')
        assert result["username"] == username
        assert result["name"] == name
        assert result["mobile"] == mobile
        assert result["role"] == role
        assert result["position"] == position
        assert result["email"] == email
        assert len(result["groups"]) == 3
        assert result["function_manage"] == 0
        assert result["tb_manage"] == 0
        assert result["data_source_manage"] == 0
        assert result["tml_manage"] == 0
        assert result["account_manage"] == 0
        assert result["has_dsh_permission"] == 1
        assert result["has_tb_permission"] == 1
        assert result["has_data_permission"] == 1
        assert result["has_dsh_manage_permission"] == 1
        assert result["has_date_filter_permission"] == 1
        # delete
        resp = openbdp.call_method_and_succ("openbdp_userdelete", uid, ret_expr='')
        assert resp["status"] == "0"
        # #清除测试数据
        resp = openbdp.call_method_and_succ("openbdp_groupdel", T, ret_expr='')
        assert resp["status"] == "0"

    def test_openbdp_manageCreate(self):
        openbdp = OpenbdpSdk.instance()
        username = "username" + str(time.time())
        name = "openbdpxianjin" + str(random.randint(0, 20))
        mobile = self.createPhone()
        password = "123qweasd",
        email = mobile + "@qq.com"
        # 2:管理员，3:普通账号 | int | 必填 |
        role = 2
        position = "position"
        # 分组信息
        pid = openbdp.call_method_and_succ("openbdp_grouplist", ret_expr='["result"][0]["group_id"]')
        gid = openbdp.call_method_and_succ("openbdp_groupcreate", name, pid, ret_expr='["result"]')
        belong_groups = [gid]
        manage_groups = [pid]
        tml_manage = 1
        function_manage = 1
        tb_manage = 1
        data_source_manage = 1
        account_manage = 1
        openbdp.openbdp_userCreate(username, name, mobile, password, role, email=email, position=position,
                                   belong_groups=belong_groups, manage_groups=manage_groups,
                                   account_manage=account_manage, tml_manage=tml_manage,
                                   function_manage=function_manage, tb_manage=tb_manage,
                                   data_source_manage=data_source_manage)
        uid = json.loads(openbdp.raw_data)["result"]
        result = openbdp.call_method_and_succ("openbdp_userInfo", uid, ret_expr='["result"]')
        assert result["username"] == username
        assert result["name"] == name
        assert result["mobile"] == mobile
        assert result["role"] == role
        assert result["position"] == position
        assert result["account_manage"] == account_manage
        assert result["function_manage"] == 1
        assert result["tb_manage"] == 1
        assert result["data_source_manage"] == 1
        assert result["tml_manage"] == 1
        assert result["manage_groups"][0]["group_id"] == pid
        # assert result["has_tb_permission"] == 1
        # assert result["has_data_permission"] == 1
        assert result["has_dsh_permission"] == 1
        # delete
        resp = openbdp.call_method_and_succ("openbdp_userdelete", uid, ret_expr='')
        assert resp["status"] == "0"
        # 清除测试数据
        resp = openbdp.call_method_and_succ("openbdp_groupdel", gid, ret_expr='')
        assert resp["status"] == "0"

    def test_admin2user(self):
        openbdp = OpenbdpSdk.instance()
        username = "username" + str(time.time())
        name = "xianjinname" + str(random.randint(0, 20))
        mobile = self.createPhone()
        password = "123qweasd",
        email = mobile + "@qq.com"
        # 2:管理员，3:普通账号 | int | 必填 |
        role = 2
        position = "position"
        # 分组信息
        pid = openbdp.call_method_and_succ("openbdp_grouplist", ret_expr='["result"][0]["group_id"]')
        manage_groups = [pid]
        account_manage = 1
        sex = 0
        openbdp.openbdp_userCreate(username, name, mobile, password, role, email=email, position=position, sex=sex,
                                   manage_groups=manage_groups, account_manage=account_manage)
        uid = json.loads(openbdp.raw_data)["result"]
        result = openbdp.call_method_and_succ("openbdp_userInfo", uid, ret_expr='["result"]')
        assert result["username"] == username
        assert result["name"] == name
        assert result["mobile"] == mobile
        assert result["role"] == role
        assert result["position"] == position
        assert result["account_manage"] == account_manage
        assert result["sex"] == "男"
        # modify 字段
        name = "modifyname" + str(random.randint(0, 20))
        mobile = self.createPhone()
        email = mobile + "@163.com"
        # 2:管理员，3:普通账号 | int | 必填 |
        role = 3
        sex = 1
        position = "modifposition"
        # userdmodify
        openbdp.openbdp_userdmodify(uid, name=name, mobile=mobile, email=email, position=position, role=role, sex=sex)
        result = openbdp.call_method_and_succ("openbdp_userInfo", uid, ret_expr='["result"]')
        assert result["username"] == username
        assert result["name"] == name
        assert result["mobile"] == mobile
        assert result["role"] == role
        assert result["position"] == position
        assert result["sex"] == "女"
        assert result["account_manage"] == 0
        # delete
        resp = openbdp.call_method_and_succ("openbdp_userdelete", uid, ret_expr='')
        assert resp["status"] == "0"

    def test_user2admin(self):
        openbdp = OpenbdpSdk.instance()
        username = "username" + str(time.time())
        name = "xianjinname" + str(random.randint(0, 20))
        mobile = self.createPhone()
        password = "123qweasd",
        email = mobile + "@qq.com"
        # 2:管理员，3:普通账号 | int | 必填 |
        role = 3
        position = "position"
        sex = 0
        openbdp.openbdp_userCreate(username, name, mobile, password, role, email=email, position=position, sex=sex)
        uid = json.loads(openbdp.raw_data)["result"]
        result = openbdp.call_method_and_succ("openbdp_userInfo", uid, ret_expr='["result"]')
        assert result["username"] == username
        assert result["name"] == name
        assert result["mobile"] == mobile
        assert result["role"] == role
        assert result["position"] == position
        assert result["sex"] == "男"
        assert result["account_manage"] == 0
        # modify 字段
        name = "modifyname" + str(random.randint(0, 20))
        mobile = self.createPhone()
        email = mobile + "@163.com"
        # 2:管理员，3:普通账号 | int | 必填 |
        role = 2
        sex = 1
        # 分组信息
        pid = openbdp.call_method_and_succ("openbdp_grouplist", ret_expr='["result"][0]["group_id"]')
        manage_groups = [pid]
        account_manage = 1
        position = "modifposition"
        # userdmodify
        openbdp.openbdp_userdmodify(uid, name=name, mobile=mobile, email=email, position=position, role=role, sex=sex,
                                    manage_groups=manage_groups, account_manage=account_manage)
        result = openbdp.call_method_and_succ("openbdp_userInfo", uid, ret_expr='["result"]')
        assert result["name"] == name
        assert result["mobile"] == mobile
        assert result["role"] == role
        assert result["position"] == position
        assert result["sex"] == "女"
        # assert result["account_manage"] == 1
        assert result["manage_groups"] != None
        # delete
        resp = openbdp.call_method_and_succ("openbdp_userdelete", uid, ret_expr='')
        assert resp["status"] == "0"

    def test_ufunmodify(self):
        openbdp = OpenbdpSdk.instance()
        username = "username" + str(time.time())
        name = "xianjinname" + str(random.randint(0, 20))
        mobile = self.createPhone()
        password = "123qweasd",
        email = mobile + "@qq.com"
        # 2:管理员，3:普通账号 | int | 必填 |
        role = 2
        position = "position"
        # 分组信息
        pid = openbdp.call_method_and_succ("openbdp_grouplist", ret_expr='["result"][0]["group_id"]')
        manage_groups = [pid]
        sex = 0
        openbdp.openbdp_userCreate(username, name, mobile, password, role, email=email, position=position, sex=sex,
                                   manage_groups=manage_groups, account_manage=1, tml_manage=1, function_manage=1,
                                   tb_manage=1, data_source_manage=1)
        uid = json.loads(openbdp.raw_data)["result"]
        result = openbdp.call_method_and_succ("openbdp_userInfo", uid, ret_expr='["result"]')
        assert result["username"] == username
        assert result["name"] == name
        assert result["mobile"] == mobile
        assert result["role"] == role
        assert result["position"] == position
        assert result["account_manage"] == 1
        assert result["sex"] == "男"
        assert result["function_manage"] == 1
        assert result["tb_manage"] == 1
        assert result["data_source_manage"] == 1
        assert result["tml_manage"] == 1
        # openbdp_ufunmodify
        openbdp.openbdp_ufunmodify(uid, account_manage=0, tml_manage=0, function_manage=0, tb_manage=0,
                                   data_source_manage=0)
        result = openbdp.call_method_and_succ("openbdp_userInfo", uid, ret_expr='["result"]')
        assert result["username"] == username
        assert result["account_manage"] == 0
        assert result["function_manage"] == 0
        assert result["tb_manage"] == 0
        assert result["data_source_manage"] == 0
        assert result["tml_manage"] == 0
        # delete
        resp = openbdp.call_method_and_succ("openbdp_userdelete", uid, ret_expr='')
        assert resp["status"] == "0"
