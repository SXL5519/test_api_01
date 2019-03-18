#-*- coding:utf-8 -*-
"""
配置接口请求方法
"""
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import ast
import random
import re

import requests
import readConfig as readConfig
import json


class ConfigHttp:

    def __init__(self,case):
        localReadConfig = readConfig.ReadConfig()
        global host, port, timeout
        host = localReadConfig.get_http("baseurl")
        port = localReadConfig.get_http("port")
        timeout = float(localReadConfig.get_http("timeout"))
        self.headers=localReadConfig.get_http("headers")
        self.case_name=case.get('case_name')
        self.method=case.get('method')
        self.url=case.get('url')
        self.header=case.get('header')
        self.data=case.get('data')
        self.update_data_Fields=case.get('update_data_Fields').split(';')
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

    def set_data(self, data):
        """
        将data转换成字典
        :param data:
        :return:
        """
        d = {}
        if data!='null':
            for param in data.split('&'):
                k, v = param.split('=')
                d[k]=v
            return d
        else:
            return d

    def find_update_data(self,r,data,**kwargs):
        """
        例：匹配 "token":"8b63876034ab4a22bbbd4c28a1d74399"
        :param r:匹配以什么开头的字符串
        :param data: 匹配的数据
        :param n:n=1时返回正则匹配全部数据
        :return:
        """
        re_str=''
        if isinstance(r,str):
            if 'keys' in kwargs and kwargs['keys'] == 'adrId':
                re_str = re.compile(',{"' + r + '":"(.*?)","province"')
            else:
                re_str = re.compile('"' + r + '":"(.*?)"')
            if len(re_str.findall(data))!=0:
                if 'n' in kwargs:
                    if kwargs['n']==1:
                        a = re_str.findall(data)
                else:
                    i = random.randint(0, len(re_str.findall(data)) - 1)
                    a = re_str.findall(data)[i]
            else:
                a='null'
            return a
        elif isinstance(r,tuple):
            list_1 = []
            data = json.loads(data)
            data_1 = data
            for a in r:
                if isinstance(data_1, list):
                    for s in range(len(data_1)):
                        if type(data_1[s][a])==int:
                            list_1 += self.set_list(str(data_1[s][a]))
                        else:
                            list_1 += self.set_list(data_1[s][a])
                    data_1 = list_1
                    list_1 = []
                elif isinstance(data_1, dict):
                    data_1 = data_1[a]
            if 'n' in kwargs:
                if kwargs['n']== 1 :
                    pass
            else:
                k = random.randint(0, len(data_1) - 1)
                data_1 = data_1[k]
            return data_1


    def find_update_data_01(self,r,data,*n):
        """
        以json格式匹配
        例：匹配 "token":"8b63876034ab4a22bbbd4c28a1d74399"
        :param r:需要匹配的json格式key值（元组）
        :param data: 匹配的数据
        :param n:n=1时返回匹配全部数据
        :return:
        """
        list_1=[]
        data=json.loads(data)
        data_1=data
        for a in r:
            if isinstance(data_1,list):
                for s in range(len(data_1)):
                    list_1+=self.set_list(data_1[s][a])
                data_1=list_1
                list_1=[]
            elif isinstance(data_1,dict):
                data_1=data_1[a]
        if n[0]==1:
            k=random.randint(0,len(data_1) - 1)
            data_1 = data_1[k]
        return data_1


    def req(self,method,url,header,data):
        if method=='post':
            # r=requests.post(url=url,headers=header,data=data,timeout=timeout,verify=False)
            r = requests.post(url=url, headers=header, data=data,verify=False)
        elif method=='get':
            # r=requests.get(url=url,headers=header,data=data,timeout=timeout)
            r = requests.get(url=url, headers=header, data=data,verify=False)
        return r

    def set_list(self,data):
        """
        将参数转变为list
        :return:
        """
        a=[]
        if type(data)==str:
            a.append(data)
            return a
        else:
            return data


