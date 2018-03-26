#!/usr/bin/python
# -*- coding: utf8 -*-
# __author__ = '5xianjin'
import pytest
from lib.iron_man.group import group
from lib.iron_man.account import Account
from lib.BdpSDK import BdpSDK
import time
import random
import json


class Test_group(object):

    def test_create_group(self):
        name = "groupname" + str(time.time())
        pid = group.grouplist()[0]["group_id"]
        gid = group.create(name, pid)
        ginfo = group.groupinfo(gid)
        assert ginfo["group_name"] == name
        assert ginfo["group_id"] == gid
        assert ginfo["parent_group_id"] == pid

    # 10层级分组
    def test_create_10group(self):
        name = "10grouptest" + str(time.time())
        pid = group.grouplist()[0]["group_id"]
        gid = group.create(name, pid)
        T = gid
        result = group.groupinfo(gid)
        assert result["group_name"] == name
        assert result["group_id"] == gid
        assert result["parent_group_id"] == pid
        count = 1
        while (count < 11):
            name = "10grouptest" + str(count) + str(time.time())
            if count == 10:
                with pytest.raises(AssertionError):
                    group.create(name, gid)
                assert json.loads(group().bdp.raw_data)["status"] == "12012"
            else:
                ggid = group.create(name, gid)
                result = group.groupinfo(ggid)
                assert result["group_name"] == name
                assert result["group_id"] == ggid
                assert result["parent_group_id"] == gid
                gid = ggid
            count = count + 1


    # 把两个二级分组修改为上下级关系
    def test_groupmodify(self):
        name = "m1groupname" + str(time.time())
        pid = group.grouplist()[0]["group_id"]
        count = 0
        while (count < 2):
            gid = group.create(name, pid)
            if count == 0:
                T = gid
            result = group.groupinfo(gid)
            assert result["group_name"] == name
            assert result["group_id"] == gid
            assert result["parent_group_id"] == pid
            count = count + 1
            name = "m2groupname" + str(time.time())
        # 修改分组2
        name1 = "bdpmodifygroupname" + str(time.time())
        # call_method_and_succ not support **kwargs
        # group.groupmodify(gid, name=name1, parent_group_id=T)
        group().bdp.groupmodify(gid, name=name1, parent_group_id=T)
        result = group.groupinfo(gid)
        assert result["group_name"] == name1
        assert result["group_id"] == gid
        assert result["parent_group_id"] == T

    # 同层级不允许分组名称相同
    def test_groupname_repeat(self):
        name = "groupname" + str(time.time())
        pid = group.grouplist()[0]["group_id"]
        gid = group.create(name, pid)
        result = group.groupinfo(gid)
        assert result["group_name"] == name
        assert result["parent_group_id"] == pid
        with pytest.raises(AssertionError):
            group.create(name, pid)
        assert json.loads(group().bdp.raw_data)["status"] == "12002"
        # 不同层级允许名称相同
        ggid = group.create(name, gid)
        result = group.groupinfo(ggid)
        assert result["group_name"] == name
        assert result["parent_group_id"] == gid


    # 增减组员、管理员
    def test_group_user_manager(self):
        name = "test_group_user_manager" + str(time.time())
        pid = group.grouplist()[0]["group_id"]
        gid = group.create(name, pid)
        result = group.groupinfo(gid)
        assert result["group_name"] == name
        assert result["group_id"] == gid
        assert result["parent_group_id"] == pid
        # 准备组员、管理员
        username = "test_group_user_manager" + str(time.time())
        password = "123qweasd"
        uid = Account.create(username, password, gid)
        uinfo = Account.subinfo(uid)
        assert uinfo['userid'] == uid
        assert uinfo['username'] == username
        assert uinfo['account_permission'] == 0
        assert uinfo['role'] == 3
        assert uinfo['manage_groups'] == []
        #is_extrace 已经废弃
        #assert uinfo['is_extrace'] == 0
        user_ids = [uid]
        # 添加组员/管理员
        group().bdp.groupmodify(gid, user_list=user_ids,manage_group_id_list=user_ids)
        result = group.groupinfo(gid)
        assert result["group_name"] == name
        assert result["group_id"] == gid
        assert result["parent_group_id"] == pid
        # assert result["manager_user_list"][0]["user_id"] == uid
        assert sorted(result["manager_user_list"])[0]["user_id"]== uid
        assert result["user_list"][0]["userid"] == uid
        # 删除组员/管理员
        uids = []
        group().bdp.groupmodify(gid, user_list=uids,manage_group_id_list=uids)
        result = group.groupinfo(gid)
        assert result["group_name"] == name
        assert result["group_id"] == gid
        assert result["parent_group_id"] == pid
        assert result["user_list"] == uids
        #清理
        Account.user_del(uid)

    # todo for create date
    def aatest_create_grup10(self):
        pid = "57eb3f2dc1e6e8d1789e7b2202193f99"
        # ls =['xianjinA00', 'xianjinB00', 'xianjinC00', 'xianjinD00','xianjinE00', 'xianjinF00', 'xianjinG00', 'H00','I00', 'J00', 'K00', 'L00','M00', 'N00','xianjinQ00', 'xianjinR00', 'xianjinS00', 'xianjinT00', 'xianjinU00', 'xianjinV00', 'xianjinW00', 'xianjinX00']
        ls = ['xianjinA00', 'apple0', 'huawei0']
        for i in ls:
            count = 0
            while (count < 10):
                name = i + str(count)
                id = group.create(name, pid)
                pid = id
                count = count + 1
            pid = "57eb3f2dc1e6e8d1789e7b2202193f99"

    def aaatest_pcreate_grup(self):
        pid = "1a23f190b94dc445e475e4ac864492ff"
        count = 0
        while (count < 2):
            name = "uuu" + str(count)
            id = group.create(name, pid)
            pid = id
            count = count + 1
