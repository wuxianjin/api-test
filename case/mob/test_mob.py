#! /usr/bin/env python
# -*- coding:utf-8 -*-
""" 
@author:xianjin 
@time: 2018-04-23-16
"""

import pytest
from lib.MobSDK import mobSdk


class Test_mob_data(object):
    @pytest.mark.parametrize("mob_sys, mob_ver", [
        ("iphone os", "3.5"),
        ("android", "3.6"),
    ])
    def test_char_data(self, mob_sys, mob_ver):
        mob = mobSdk.instance()
        ctid = 'ct_c43908d43f3f61eec412094f5876365c'
        res = mob.call_method_and_succ("mob_chart_data", mob_sys, mob_ver, ctid, ret_expr='["result"]')
        assert res['data']['show_sub_dimension'] == False
        assert res['data_mng'] == 'MobDataMng'
