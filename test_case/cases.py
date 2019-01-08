#-*- coding:utf-8 -*-
import ast

import ddt
import requests

from configHttp import ConfigHttp
from initial_file import MyTest
from read_data_file import get_all_data
from db_file import DB
from function import screen_shot



"""
测试用例
"""
@ddt.ddt
class AA(MyTest):

    dicts = {}

    @ddt.data(*get_all_data().get('data_file_01'))
    def test_01(self,case):
        case=ConfigHttp(case)
        print('用例名称：'+case.case_name)
        url=case.set_url(case.url)
        print('接口地址：'+url)
        print('请求方式：'+case.method)
        if case.header!='null':
            header = ast.literal_eval(case.header)
            header['Authorization']=self.dicts['token']
        else:
            header=''
        print('请求头：'+str(header))
        if len(case.update_data_Fields)>1:
            if case.update_data_Fields[0]=='0':
                data = case.set_data(case.data)
                print('请求参数：' + str(data))
                r=case.req(case.method,url,header,data)
                for i in case.update_data_Fields[1:]:
                    self.dicts[i]=case.find_update_data(i,r.text)
            elif case.update_data_Fields[0]=='1':
                data = case.set_data(case.data)
                for i in case.update_data_Fields[1:]:
                    if i=='userId':
                        a='id'
                        data[i] = self.dicts[a]
                    else:
                        data[i]=self.dicts[i]
                print('请求参数' + str(data))
                r=case.req(case.method,url,header,data)
        else:
            data = case.set_data(case.data)
            print('请求参数：' + str(data))
            r = case.req(case.method, url, header, data)
        print('响应数据：'+r.text)
        self.assertEqual(r.status_code, 200,'状态码错误')
        for c in case.assert_msg:
            print('断言：'+c)
            self.assertIn(c,r.text,'响应错误')
        print('全局字典：'+str(self.dicts))







