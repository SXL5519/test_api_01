#-*- coding:utf-8 -*-
"""
配置接口请求方法
"""
import ast
import re

import requests
import readConfig as readConfig
import json


class ConfigHttp:

    def __init__(self,case):
        # print(case)
        localReadConfig = readConfig.ReadConfig()
        global host, port, timeout
        host = localReadConfig.get_http("baseurl")
        port = localReadConfig.get_http("port")
        timeout = float(localReadConfig.get_http("timeout"))
        ###将字符串转化成字典
        # headers = ast.literal_eval(localReadConfig.get_http("headers"))
        # self.params = {}
        # self.data = {}
        # # self.data = json.dumps({})
        # self.url = None
        # self.files = {}
        # self.headers={}
        self.case_name=case.get('case_name')
        self.method=case.get('method')
        self.url=case.get('url')
        self.header=case.get('header')
        self.data=case.get('data')
        self.update_data_Fields=case.get('update_data_Fields').split(',')
        self.sql_Table=case.get('sql_Table')
        self.sql_query_statement=case.get('sql_query_statement')
        self.assert_msg=case.get('assert_msg').split(';')
    def set_url(self, url):
        """
        组装URL
        :param url:
        :return:
        """
        url = host + url
        return url
        # print(self.url)
        # return self.url

    # def set_headers(self, header):
    #     self.headers = ast.literal_eval(header)
    #
    # def convert_set_headers(self,headers):
    #     self.headers=headers
    #
    # def set_params(self, param):
    #
    #     self.params = ast.literal_eval(param)
    #
    def set_data(self, data):
        """
        将data转换成字典
        :param data:
        :return:
        """
        d = {}
        for param in data.split('&'):
            k, v = param.split('=')
            d[k]=v
        return d

    def find_update_data(self,r,data):
        """
        例：匹配 "token":"8b63876034ab4a22bbbd4c28a1d74399"
        :param r:匹配以什么开头的字符串
        :param data: 匹配的数据
        :return:
        """
        re_str=re.compile('"'+r+'":"(.*?)"')
        if len(re_str.findall(data))!=0:
            a = re_str.findall(data)[0]
        else:
            a='null'
        return a



    # def convert_set_data(self, data):
    #     """
    #     组装修改后的data ，不需要改变变量类型
    #     :param data:
    #     :return:
    #     """
    #     self.data =data
    #
    # def set_files(self, file):
    #     """
    #     上传文件接口，组装file
    #     :param file:
    #     :return:
    #     """
    #     self.files = ast.literal_eval(file)

    # defined http get method
    def req(self,method,url,header,data):
        if method=='post':
            r=requests.post(url=url,headers=header,data=data)
        elif method=='get':
            r=requests.get(url=url,headers=header,data=data)
        return r




# if __name__ == "__main__":
#     a=ConfigHttp()
#     a.set_url("/hxwj-wkj-controller/act/bigsurprise/subPage.do")
#     a.set_data({'surpriseId':'454'})
#     a.set_headers({'User-Agent':'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Mobile Safari/537.36'})
#     print(a.post())
#     print(a.post().url)
#     print(a.post().status_code)
#     print(a.post().headers)
#     print(a.post().json())
#     # print(a.post().content)