#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ = '5xianjin'

from lib.openbdp_sdk import OpenbdpSdk
import gzip
from conf import apiconf
import time
import csv
import os


class TestOpenbdpTableCase:
    def un_gz(self, file_name):
        f_name = file_name.replace(".gz", "")
        # 创建gzip对象
        g_file = gzip.GzipFile(file_name)
        # gzip对象用read()打开后，写入open()建立的文件中
        open(f_name, "w+").write(g_file.read())
        g_file.close()

    def test_openbdp_tb_down(self):
        openbdp = OpenbdpSdk.instance()
        t = Table.from_lines([
            "date,name,value,key",
            "2012-12-29 23:59:59, A1, 1, key1",
            "2012-12-30 00:00:00, A2, 2, key2",
            "2012-12-31 00:00:00, A1, 3, key3",
            "2013-01-01 00:00:00, A2, 4, key4",
            "2013-01-02 00:00:00, A1, 5, key5",
        ])

        task_id = openbdp.call_method_and_succ("openbdp_tb_export", t.tb_id(), ret_expr='["result"]')
        time.sleep(3)
        export_status = openbdp.call_method_and_succ("openbdp_tb_status", task_id,
                                                     ret_expr='["result"]["export_status"]')
        # 可下载状态
        assert export_status == 0
        r = openbdp.openbdp_tb_down(task_id)
        fname = apiconf.DOWNLOAD_DIR + "openbdptbdown.csv.gz"
        with open(fname, "wb") as file:
            file.write(r.content)

        # 解压
        self.un_gz(fname)
        fcsv = fname.replace(".gz", "")
        with open(fcsv, 'rb') as f:
            reader = csv.reader(f)
            list = []
            for row in reader:
                list.append(row)

        assert len(list) == 6
        assert list[0] == ['date', 'name', 'value', 'key']
        assert list[5] == ['2013-01-02 00:00:00', 'A1', '5', 'key5']
        os.remove(fname)
        os.remove(fcsv)
