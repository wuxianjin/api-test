#!/usr/bin/python
# -*- coding: utf8 -*-
# __author__ = '5xianjin'
import pytest
from lib.iron_man.account import Account
from lib.iron_man.group import group
import time
from lib.BdpSDK import BdpSDK
import json
from conf import bdpconf


class Test_account(object):
    # todo for create date
    def aatest_xianjincreate_user(self):
        count = 0
        mobile = 1800000000
        while (count < 1):
            username = "xianjin" + str(count)
            uid = Account.create(username, "123qweasd", mobile)
            count = count + 1
            mobile = mobile + 1

    # 普通用户的创建、冻结、解冻、删除
    def test_create_user(self):
        username = "name" + str(time.time())
        password = "123qweasd"
        # 用户所属分组
        pid = group.grouplist()[0]["group_id"]
        gid = group.create(username, pid)
        ginfo = group.groupinfo(gid)
        assert ginfo["group_name"] == username
        assert ginfo["group_id"] == gid
        assert ginfo["parent_group_id"] == pid
        # 测试创建普通用户
        uid = Account.create(username, password, gid)
        uinfo = Account.subinfo(uid)
        assert uinfo['userid'] == uid
        assert uinfo['username'] == username
        assert uinfo['account_permission'] == 0
        assert uinfo['role'] == 3
        assert uinfo['manage_groups'] == []
        # 测试冻结
        sta = Account.userfrozen(uid, 1)
        with pytest.raises(AssertionError):
            Account.user_login(username, password)
        assert json.loads(BdpSDK.instance().raw_data)["status"] == "1029"
        # 测试解冻
        Account.userfrozen(uid, 0)
        # res = Account.user_login(username, pw)
        # assert res["result"] is not None
        # 清除测试数据
        Account.user_del(uid)

    # 管理员的创建、冻结、解冻、删除
    def test_create_adminuser(self):
        username = "name" + str(time.time())
        password = "123qweasd"
        # 管理员管理分组
        pid = group.grouplist()[0]["group_id"]
        gid = group.create(username, pid)
        ginfo = group.groupinfo(gid)
        assert ginfo["group_name"] == username
        assert ginfo["group_id"] == gid
        assert ginfo["parent_group_id"] == pid
        # 测试创建管理员
        uid = Account.create(username, password, gid, admin=True)
        uinfo = Account.subinfo(uid)
        assert uinfo['userid'] == uid
        assert uinfo['username'] == username
        assert uinfo['account_permission'] == 0
        assert uinfo['role'] == 2
        assert uinfo['manage_groups'][0]['group_id'] == gid
        # 测试冻结
        sta = Account.userfrozen(uid, 1)
        assert sta['status'] == "0"
        with pytest.raises(AssertionError):
            Account.user_login(username, password)
        assert json.loads(BdpSDK.instance().raw_data)["status"] == "1029"
        # 测试解冻
        Account.userfrozen(uid, 0)
        # 清除数据
        Account.user_del(uid)

    def aatest_uinfo(self):
        sta = Account().user_login("500", "123qweasd")
        assert sta['status'] == "0"

    def _preuser(self):
        username = "preuser" + str(time.time())
        password = "123qwead"
        # 用户所属分组
        pid = group.grouplist()[0]["group_id"]
        gid = group.create(username, pid)
        ginfo = group.groupinfo(gid)
        assert ginfo["group_name"] == username
        assert ginfo["group_id"] == gid
        assert ginfo["parent_group_id"] == pid
        # 测试创建普通用户
        uid = Account.create(username, password, gid)
        uinfo = Account.subinfo(uid)
        assert uinfo['userid'] == uid
        assert uinfo['username'] == username
        assert uinfo['account_permission'] == 0
        assert uinfo['role'] == 3
        assert uinfo['manage_groups'] == []
        return uid, gid

    def test_userreset_pwd(self):
        uid, gid = self._preuser()
        # 处于重置密码状态
        Account.reset_pwd(uid)
        uinfo = Account.subinfo(uid)
        assert uinfo['status'] == 2
        # 重新设定密码
        repassword = "1234qweasd"
        Account.init_pwd(uid, repassword)
        uinfo = Account.subinfo(uid)
        assert uinfo['status'] == 0
        # 清除数据
        Account.user_del(uid)

    # 企业域内用户名唯一
    def test_doubleusername(self):
        uid, gid = self._preuser()
        uinfo = Account.subinfo(uid)
        username = uinfo['username']
        with pytest.raises(AssertionError):
            Account.create(username, "123qweasd", gid)
        assert json.loads(BdpSDK.instance().raw_data)["status"] == "8003"

    # 普通用户修改为管理员
    def test_account_permission(self):
        uid, gid = self._preuser()
        uname = "修改的名字"
        uemail = "youxiang" + str(int(time.time())) + "@gmail.com"
        usex = "女"
        uposition = "修改的职位"
        # "mobile": umobile,
        userinfo = {"name": uname, "email": uemail, "sex": usex, "position": uposition,
                    "role": 2, "manage_group_id_list": [gid],
                    "join_group_id_list": [gid]}
        Account().bdp.usermodify(uid, userinfo)
        # 新增api/sub/func_modify
        uinf2 = {"dsh_permission": 1, "dsh_manage": 1, "tb_permission": 1, "data_permission": 1,
                 "machine_learning_permission": 1, "data_screen": 1, "date_filter_permission": 1, "function_manage": 1,
                 "tb_manage": 1, "data_source_manage": 1, "tml_manage": 1, "account_permission": 1, "role": 2}
        Account().bdp.funcmodify(uid, uinf2)
        uinfo = Account.subinfo(uid)
        assert uinfo['userid'] == uid
        assert uinfo['account_permission'] == 1
        assert uinfo['dsh_permission'] == 1
        assert uinfo['dsh_manage'] == 1
        assert uinfo['tb_permission'] == 1
        assert uinfo['data_permission'] == 1
        assert uinfo['data_screen'] == 1
        assert uinfo['date_filter_permission'] == 1
        assert uinfo['function_manage'] == 1
        assert uinfo['tb_manage'] == 1
        assert uinfo['data_source_manage'] == 1
        assert uinfo['tml_manage'] == 1
        assert uinfo['role'] == 2
        assert uinfo['manage_groups'][0]['group_id'] == gid
        assert uinfo['name'] == uname
        assert uinfo['sex'] == usex
        assert uinfo['position'] == uposition
        assert uinfo['email'] == uemail
        assert len(uinfo['groups']) == 2
        # 清除数据
        Account.user_del(uid)
