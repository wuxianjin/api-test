#!/usr/bin/python
# -*- coding: utf8 -*-

import time


class BaseCase:
    """

    """

    def _create_field(self, bdp, tb, f_name, params={}, formula="", flag=0, data_type="string"):

        bdp.call_method_and_succ("field_create", tb.tb_id(), f_name, formula, data_type, "", flag, params)

        schema = bdp.call_method_and_succ("tb_info", tb.tb_id(), ret_expr='["result"]["schema"]')

        for i in schema:
            if f_name == i["name"]:
                return tb.field_from_resp(i)

        assert False

    def create_group_field(self, bdp, tb, params, f_name=""):

        if not f_name:
            f_name = str(time.time())

        return self._create_field(bdp, tb, f_name, params=params)

    def create_tb_calc_field(self, bdp, tb, f_name, formula, data_type="string"):

        return self._create_field(bdp, tb, f_name, formula=formula, flag=1, data_type=data_type)

    def create_ct_calc_field(self, bdp, tb, f_name, formula, data_type="string"):

        return self._create_field(bdp, tb, f_name, formula=formula, flag=0, data_type=data_type)

    def tear_down(self):

        for i in self.fd_list:
            self.bdp.call_method_and_succ("field_delete", i["tb_id"], i["f_name"])

    def gen_num_fixed_group(self, fid, num_range, step):

        assert isinstance(num_range, list)

        params = {
            "type": "group",
            "info": {
                "default": "未分组",
                "type": "fixed",
                "range": num_range,
                "step": step
            },

            "fid": fid,
            "data_type": "number"
        }

        return params

    def gen_num_custom_group(self, fid, range_list):

        assert isinstance(range_list, list)

        # range_list = [
        #     [[1, 2], [0, 0], "test"],
        #     []
        # ]

        params = {
            "type": "group",
            "info": {
                "default": "未分组",
                "type": "custom",
                "groups": [
                    {"range": r, "boundary": b, "name": n}
                    for r, b, n in range_list
                ]
            },
            "fid": fid,
            "data_type": "number"
        }

        return params

    def gen_string_simple_contain(self, fid, item_list, info_data_type=""):

        complex_list = [
            [i[0], "AND", [{"operator": 1, "value": i[1]}]]
            for i in item_list
        ]

        return self.gen_string_group(fid, complex_list, info_data_type)

    def gen_string_simple_eq(self, fid, item_list, info_data_type=""):

        complex_list = [
            [i[0], "AND", [{"operator": 0, "value": i[1]}]]
            for i in item_list
        ]

        return self.gen_string_group(fid, complex_list, info_data_type)

    def gen_string_simple_exclude(self, fid, item_list, info_data_type=""):

        complex_list = [
            [i[0], "AND", [{"operator": 2, "value": i[1]}]]
            for i in item_list
        ]

        return self.gen_string_group(fid, complex_list, info_data_type)

    def gen_string_group(self, fid, item_list, info_data_type=""):

        # item_list = [
        #     ["test1", "AND", [{"operator": 0, "value": 2}, {}]]
        # ]

        params = {
            "type": "group",
            "info": {
                "default": "未分组",
                "groups": [
                    {"name": n, "logic": l, "conditions": c_list}
                    for n, l, c_list in item_list
                ]
            },
            "fid": fid,
            "data_type": "string"
        }
        if not info_data_type:
            params["info"]["type"] = "condition"

        return params

    def gen_expr_group(self, data_type, fid, item_list):

        # item_list = [
        #     ["test1", "[2010-1-1]>21"]
        # ]

        params = {
            "type": "group",
            "info": {
                "default": u"未分组",
                "type": "expression",
                "groups": [
                    {"name": n, "expression": e}
                    for n, e in item_list
                ]
            },
            "fid": fid,
            "data_type": data_type,
        }

        return params

    def gen_date_expr_group(self, fid, item_list):

        data_type = "date"

        return self.gen_expr_group(data_type, fid, item_list)

    def gen_string_expr_group(self, fid, item_list):

        data_type = "string"

        return self.gen_expr_group(data_type, fid, item_list)

    def gen_number_expr_group(self, fid, item_list):

        data_type = "number"

        return self.gen_expr_group(data_type, fid, item_list)

    def gen_date_group_normal(self, fid, day_list):

        # day_list = [
        #     [["2012-01-01", "2013-01-01"], "myname"]
        # ]

        params = {
            "type": "group",
            "info": {
                "default": "未分组",
                "type": "custom",
                "groups": [
                    {"range": r_list, "name": n}
                    for r_list, n in day_list
                ]
            },

            "fid": fid,
            "data_type": "date"
        }

        return params

    def gen_date_group_year(self, fid, day_list):

        # day_list = [
        #     [["0101", "0202"], "test"]
        # ]

        params = {
            "type": "group",
            "info": {
                "default": "未分组",
                "type": "group_year",
                "groups": [
                    {"range": rl, "name": n}
                    for rl, n in day_list
                ]
            },
            "fid": fid,
            "data_type": "date"
        }

        return params

    def gen_date_group_month(self, fid, day_list):

        # day_list = [
        #     [[1, 15], "test"]
        # ]

        for i in day_list:
            assert [type(j) for j in i[0]] == [type(0), type(0)]

        params = {
            "type": "group",
            "info": {
                "default": "未分组",
                "type": "group_month",
                "groups": [
                    {"range": rl, "name": n}
                    for rl, n in day_list
                ]
            },
            "fid": fid,
            "data_type": "date"
        }

        return params

    def gen_date_group_week(self, fid, day_list):

        # day_list = [
        #     [[1, 3], "test"]
        # ]

        for i in day_list:
            assert [type(j) for j in i[0]] == [type(0), type(0)]

        params = {
            "type": "group",
            "info": {
                "default": "未分组",
                "type": "group_week",
                "groups": [
                    {"range": rl, "name": n}
                    for rl, n in day_list
                ]
            },
            "fid": fid,
            "data_type": "date"
        }

        return params

    def gen_date_group_fixed_quarter(self, fid, start_year, start_q, step):

        return self.gen_date_group_fixed(fid, "quarter", [str(start_year), str(start_q)], step)

    def gen_date_group_fixed_month(self, fid, start_year, start_m, step):

        return self.gen_date_group_fixed(fid, "month", [str(start_year), str(start_m)], step)

    def gen_date_group_fixed_year(self, fid, start_year, step):

        return self.gen_date_group_fixed(fid, "year", [str(start_year)], step)

    def gen_date_group_fixed_day(self, fid, start_date, step):

        return self.gen_date_group_fixed(fid, "day", [start_date], step)

    def gen_date_group_fixed_week(self, fid, start_year, start_w, step):

        return self.gen_date_group_fixed(fid, "week", [str(start_year), str(start_w)], step)

    def gen_date_group_fixed(self, fid, aggr, start, step):

        assert aggr in ("quarter", "year", "month", "day", "week")

        params = {
            "type": "group",
            "info": {
                "default": "未分组",
                "type": "fixed",
                "aggregator": aggr,
                "start": start,
                "step": step
            },
            "fid": fid,
            "data_type": "date"
        }

        return params





