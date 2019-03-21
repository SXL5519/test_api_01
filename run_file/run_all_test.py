# -*- coding: utf-8 -*-
"""
运行文件
"""

import unittest,time,sys,os
path=os.path.split(sys.path[0])[0]
sys.path.append(path)
sys.path.append(path+'\\test_case')
# sys.path.append(path+'/run_file')
# print(sys.path)
from HTMLTestRunner_PY3 import HTMLTestRunner
from function import send_mail,screen_shot,logfile
case_dir = "test_case"
pattern="*cases.py"
# pattern="*case_01.py"
discover = unittest.defaultTestLoader.discover(case_dir,pattern)



if __name__ =='__main__':
    # logfile()
    #日期格式化
    times = time.strftime("%Y%m%d%H%M%S")
    report_file=path+"/report/"+times+"-testresult.html"
    # report_file ="../report/" + times + "-testresult.html"####本地运行
    fp = open(report_file,"wb")
    runner = HTMLTestRunner(stream=fp,
                            title="接口自动化测试报告",
                            description="运行环境：Python")
    runner.run(discover)
    fp.close()
    send_mail(1,report_file)