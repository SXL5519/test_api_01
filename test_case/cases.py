#-*- coding:utf-8 -*-
import ast
import random

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
    goods=[]
    addr = []

    @ddt.data(*get_all_data().get('data_file_01'))
    def test(self,case):
        a=0

        case=ConfigHttp(case)
        print('用例名称：'+case.case_name)
        url=case.set_url(case.url)
        print('接口地址：'+url)
        print('请求方式：'+case.method)
        if case.header!='null':
            header = ast.literal_eval(case.headers)
            header['Authorization']=self.dicts['tokenID']
        else:
            header=''
        print('请求头：'+str(header))
        if len(case.update_data_Fields)>1:
            if case.update_data_Fields[0]=='0':
                data = case.set_data(case.data)
                print('请求参数：' + str(data))
                r=case.req(case.method,url,header,data)
                for i in case.update_data_Fields[1:]:
                    i_one=tuple(eval(i))
                    if i_one[1] in self.dicts.keys():###需要更新的字段已经存在在全局字典中
                        for j in range(len(self.goods)):###防止放入重复的数据
                            if case.find_update_data(i_one[0],r.text,keys=0) not in self.goods[j]:
                                a=1
                        if a==1:
                            self.goods.append(case.set_list(case.find_update_data(i_one[0],r.text,keys=0)))
                        else:
                            self.dicts[i_one[1]]=self.goods
                    else:
                        if i_one[1]=='goodsId':
                            self.goods.append(case.set_list(case.find_update_data(i_one[0], r.text,keys=0)))
                            self.dicts[i_one[1]] = self.goods
                        else:
                            self.dicts[i_one[1]]=case.find_update_data(i_one[0],r.text,keys=0)
            elif case.update_data_Fields[0]=='1':
                data = case.set_data(case.data)
                for i in case.update_data_Fields[1:]:
                    i_one = tuple(eval(i))
                    if i_one[0] =='goodsId':
                        j=random.randint(0,len(self.dicts['goodsId'])-1)
                        data[i_one[1]]=self.dicts[i_one[0]][j][0]
                    else:
                        data[i_one[1]]=self.dicts[i_one[0]]
                print('请求参数:' + str(data))
                r=case.req(case.method,url,header,data)
            elif case.update_data_Fields[0] == '2':
                data = case.set_data(case.data)
                for i in case.update_data_Fields[1:]:
                    i_one = tuple(eval(i))
                    print(i_one)
                    if i_one[0][0] == 'goodsId':
                        j = random.randint(0, len(self.dicts['goodsId']) - 1)
                        data[i_one[0][1]] = self.dicts[i_one[0][0]][j][0]
                    else:
                        data[i_one[0][1]] = self.dicts[i_one[0][0]]
                print('请求参数:' + str(data))
                r = case.req(case.method, url, header, data)
                for i in case.update_data_Fields[1:]:
                    i_one=tuple(eval(i))
                    if i_one[1][1] in self.dicts.keys():###需要更新的字段已经存在在全局字典中
                        for j in range(len(self.goods)):###防止放入重复的数据
                            if case.find_update_data(i_one[1][0],r.text) not in self.goods[j]:
                                a=1
                        if a==1:
                            self.goods.append(case.set_list(case.find_update_data(i_one[1][0],r.text,keys=0)))
                        else:
                            self.dicts[i_one[1][1]]=self.goods
                    else:
                        if i_one[1][1]=='goodsId':
                            self.goods.append(case.set_list(case.find_update_data(i_one[1][0], r.text,keys=0)))
                            self.dicts[i_one[1][1]] = self.goods
                        elif i_one[1][1]=='aid':
                            self.dicts[i_one[1][1]]=case.find_update_data(i_one[1][0], r.text,keys='aid')
                        else:
                            self.dicts[i_one[1][1]]=case.find_update_data(i_one[1][0],r.text,keys=0)
        else:
            if case.data!='null':
                data = case.set_data(case.data)
                print('请求参数：' + str(data))
                r = case.req(case.method, url, header, data)
            else:
                data=case.data
                print('请求参数：' + str(data))
                r = case.req(case.method, url, header, data)
        print('响应数据：'+r.text)
        self.assertEqual(r.status_code, 200,'状态码错误')
        for c in case.assert_msg:
            print('断言：'+c)
            self.assertIn(c,r.text,'响应错误')
        print('全局字典：'+str(self.dicts))







