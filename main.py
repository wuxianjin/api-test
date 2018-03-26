#!/usr/bin/python
# -*- coding: utf8 -*-

import sys
import pytest
import traceback
import Queue
import os
import re
import time
import select
from conf import apiconf
from util import util


# default encoding
reload(sys)
print "current encoding is %s" % sys.getdefaultencoding()
sys.setdefaultencoding('utf-8')

# add search path
sys.path.append('./')

bdp_run_mode = ("format_space", "create_data")


class PipeFile(object):

    def __init__(self, fd):
        self.fd = fd
        self.buf = ""

    def fileno(self):
        return self.fd

    def readlines(self):

        self.buf += os.read(self.fd, 65535 * 1000)

        lines = self.buf.split("\n")

        self.buf = lines[-1]

        return lines[:-1]


def casefilter(line):

    m = re.match(r" *<Function '([^\[\]]*)(\[.*\])?'>", line)

    case_name = m.expand(r"\1") if m else ""

    return case_name


def case_list(mark="", is_reversed=False):

    oldstd = sys.stdout

    fp = open("./case.list", "w")

    py_args = ["--collect-only"]

    if mark:
        py_args.append("-m")
        mark_param = ("not %s" % mark) if is_reversed else mark
        py_args.append(mark_param)

    try:
        sys.stdout = fp
        pytest.main(args=py_args)
    finally:
        sys.stdout = oldstd
        fp.close()

    fp = open("./case.list", "r")
    result = [casefilter(line) for line in fp]
    fp.close()

    valid_result = [item for item in result if item]
    valid_result.sort()

    case_count = len(valid_result)
    index = 1
    while index <= case_count - 1:
        if valid_result[index].startswith(valid_result[index - 1]):
            del valid_result[index]
            index -= 1
            case_count = len(valid_result)

        index += 1

    return set(valid_result)


def result_processor():

    fname = "raw_result_%s.txt" % time.strftime("%F")
    fp = open(fname, "w")

    failed_count = 0
    succ_count = 0
    total_count = 0

    failed_list = list()

    def _refresh_info():

        def _refresh_for_mac():

            os.system("clear")

            for i in failed_list:
                print "%s Failed" % i

            print "testing \33[32m%s, \33[0min account:\33[32m[%s]\33[0m" % (apiconf.API_HOST, apiconf.USER_NAME)
            print "\33[32m%d passed\33[0m, \33[31m%d failed\33[0m, %d total" % (succ_count, failed_count, total_count)

        def _refresh_for_jenkis():

            for i in failed_list:
                print "%s" % i

            print "%d passed, %d failed, %d total" % (succ_count, failed_count, total_count)

        if util.plat_form() == "Mac":
            _refresh_for_mac()
        else:
            _refresh_for_jenkis()

    try:
        while True:
            line = yield
            fp.write(time.strftime("%X") + line + "\n")

            mprefix = re.match(r"\[processor\d+\] (.*)", line)

            if not mprefix:
                continue

            line = mprefix.expand(r"\1")

            if total_count == 0:
                m = re.match(r".*collected (\d+) items", line)
                if m:
                    total_count = int(m.expand(r"\1"))
                continue

            m = re.match(r"case.*::(.*)::(.*) FAILED", line)
            if m:
                failed_count += 1
                failed_list.append(m.expand(r"\2"))
                _refresh_info()
            elif re.match(r"case.*::(.*)::(.*) PASSED", line):
                succ_count += 1
                _refresh_info()

    except StopIteration:
        pass

    finally:
        # 检查case数是否正确
        fp.close()
        assert succ_count + failed_count == total_count


def colect_result(fds):

    processor = result_processor()
    processor.next()

    file_objs = [PipeFile(i) for i in fds]

    while True:
        rds = select.select(file_objs, [], [], apiconf.WAIT_TIME_OUT)

        if not rds[0]:
            print "wait for fd timeout:[%s], at %s" % (apiconf.WAIT_TIME_OUT, time.strftime("%H:%M:%S"))
            break

        items = []
        for fd in rds[0]:
            # it = i for i in fd.readlines()
            # pdb.set_trace()
            _iter_prefix = ("[processor%d] %s" % (fd.fileno(), i) for i in fd.readlines())
            items += list(_iter_prefix)

        for line in items:
            processor.send(line)

    processor.close()


def multi_run():

    q_list = [Queue.Queue() for _ in xrange(0, apiconf.PROCESS_COUNT)]
    pids = list()
    pipes = list()

    index = 0
    for case in case_list(mark="single", is_reversed=True):
        # 第一步找出所有没有特殊要求的case，打散了跑，没有特殊需求是指可以并发跑不会冲突的
        q_list[(index % (apiconf.PROCESS_COUNT-1)) if apiconf.PROCESS_COUNT > 1 else 0].put(case)
        index += 1

    for case in case_list(mark="single", is_reversed=False):
        # 第二步找出必须串行跑得case，单独放在一个进程跑
        q_list[apiconf.PROCESS_COUNT-1].put(case)

    for i in xrange(0, apiconf.PROCESS_COUNT):

        r, w = os.pipe()
        pid = os.fork()
        if pid == 0:

            class _PFile:
                def write(self, a_str):
                    os.write(w, a_str)

                def flush(self):
                    pass

            sys.stdout = _PFile()
            while not q_list[i].empty():
                kp = q_list[i].get()
                print "Now picking up case %s" % kp
                pytest.main(args=["-k", kp, "-v"])

            print "I'm exit"

            return

        else:
            pipes.append(r)
            pids.append(pid)

    try:
        colect_result(pipes)
    finally:
        os.system("kill %s" % " ".join([str(i) for i in pids]))


if util.plat_form() == "Mac":
    print "testing \33[32m%s, \33[0min account:\33[32m[%s]\33[0m" % (apiconf.API_HOST, apiconf.USER_NAME)
else:
    print "testing %s, in account:[%s]" % (apiconf.API_HOST, apiconf.USER_NAME)

# mode ?
if len(sys.argv) >= 2 and sys.argv[1].startswith("--") and sys.argv[1][2:] in bdp_run_mode:
    try:
        eval("meta_data.%s()" % sys.argv[1][2:])
        exit(0)
    except Exception, e:
        print "exception occured: %s, trace_bak is\n %s" % (e.message, traceback.format_exc())
        exit(1)
elif len(sys.argv) == 1:
    multi_run()
else:
    pytest.main(args=sys.argv[1:])