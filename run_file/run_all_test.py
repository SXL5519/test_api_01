# -*- coding: utf-8 -*-
"""
运行文件
"""
import unittest,time
from HTMLTestRunner_PY3 import HTMLTestRunner
from function import send_mail,screen_shot,logfile
case_dir = "../test_case"
pattern="*cases.py"
discover = unittest.defaultTestLoader.discover(case_dir,pattern)


if __name__ =='__main__':
    logfile()
    #日期格式化
    times = time.strftime("%Y%m%d%H%M%S")
    report_file="../report/"+times+"-testresult.html"
    fp = open(report_file,"wb")
    runner = HTMLTestRunner(stream=fp,
                            title="接口自动化测试报告",
                            description="运行环境：Python")
    runner.run(discover)
    fp.close()
    send_mail(1,report_file)