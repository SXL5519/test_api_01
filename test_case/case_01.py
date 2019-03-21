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
        if case.header!='null' and case.header!='':
            header=self.updata_token(case.header,case.headers)
        else:
            header=''
            print('请求头：'+str(header))
        updata_data=case.update_data_Fields[1:]
        if len(case.update_data_Fields)>1:
            data = case.set_data(case.data)
            if case.update_data_Fields[0]=='0':
                print('请求参数：' + str(data))
                r=case.req(case.method,url,header,data)
                self.update_data_Fields_0(case,r.text,updata_data)
            elif case.update_data_Fields[0]=='1':
                self.updata_data_Fields_1(data,updata_data)
                print('请求参数:' + str(data))
                r=case.req(case.method,url,header,data)
            elif case.update_data_Fields[0] == '2':
                aa = random.randint(0, len(self.dicts['goodsId']) - 1)
                self.updata_data_Fields_2(data,aa,updata_data)
                print('请求参数:' + str(data))
                r = case.req(case.method, url, header, data)
                self.updata_data_Fields_2_updata_dicts(case,r.text,aa,updata_data)
            elif case.update_data_Fields[0] == '3':
                self.updata_data_Fields_1(data,updata_data)
                print('请求参数:' + str(data))
                r = case.req(case.method, url, header, data)
                self.updata_IN_dicts_value(case,r.text,updata_data)
            elif case.update_data_Fields[0] == '4':
                self.updata_data_Fields_4(case,data,updata_data)
                print('请求参数:' + str(data))
                r = case.req(case.method, url, header, data)
            elif case.update_data_Fields[0] =='5':
                self.updata_data_Fields_5(case,data,updata_data)
                print('请求参数:' + str(data))
                r = case.req(case.method, url, header, data)
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



    def updata_token(self,header,headers):
        """
        更改token
         :param header:CSV文件header数据
          :param headers:配置文件的header数据
        :return:接口请求header
        """
        header = ast.literal_eval(header)
        if header['keys'] == 1:
            header = ast.literal_eval(headers)
            header['Authorization'] = self.dicts['tokenID']
        elif header['keys'] == 2:
            header = ast.literal_eval(headers)
            header['Authorization'] = self.dicts['sign_in_tokenID']
        else:
            header = ''
        print('请求头：' + str(header))
        return header

    def update_data_Fields_0(self,case,data,updata_data):
        """
        将接口的响应写入全局字典；
        例：0;('id','userId')  / 0;('id','userId');('token','tokenID') / 0;(('data','id'),'userId')
        第一个参数为response 返回字段，第二个为存入全局字典key
        ('data','id')为匹配json类型字段
        :param case: case对象
        :param data: 接口响应
        :return:
        """
        a=0
        for i in updata_data:
            i_one = tuple(eval(i))
            if i_one[1] in self.dicts.keys():  ###需要更新的字段已经存在在全局字典中
                for j in range(len(self.goods)):  ###防止放入重复的数据
                    for q in range(len(self.goods[j])):
                        if case.find_update_data(i_one[0], data) not in self.goods[j][q]:
                            a = 1
                if a == 1:
                    self.goods.append(case.set_list(case.find_update_data(i_one[0], data)))
                    self.dicts[i_one[1]] = self.goods
                else:
                    self.dicts[i_one[1]] = self.goods
            else:
                if i_one[1] == 'goodsId':
                    self.goods.append(case.set_list(case.find_update_data(i_one[0], data)))
                    self.dicts[i_one[1]] = self.goods
                if i_one[1] == 'merchanttypeId':
                    self.dicts[i_one[1]] = case.find_update_data(i_one[0], data)
                else:
                    self.dicts[i_one[1]] = case.find_update_data(i_one[0], data)

    def updata_data_Fields_1(self,data,updata_data):
        """
        读取全局字典里的值
        例：1;('userId','userId') / 1;('shoppcartId','shoppingCarts');('userId','userId')
        第一个字段为全局字典里的key,第二个为请求参数字段名
        :param case:case对象
        :param data:CSV文件data数据
        :return:
        """
        for i in updata_data:
            i_one = tuple(eval(i))
            if isinstance(i_one[0], tuple):
                if i_one[0][0] == 'userbankId':
                    data[i_one[1]] = self.dicts[i_one[0][0]][0][i_one[0][1]]
            else:
                if i_one[0] == 'goodsId' and i_one[1] != 'skuId':
                    j = random.randint(0, len(self.dicts['goodsId']) - 1)
                    data[i_one[1]] = self.dicts[i_one[0]][j][0]
                elif i_one[0] == 'goodsId' and i_one[1] == 'skuId':
                    data[i_one[0]] = self.dicts[i_one[0]][self.dicts['nu']][0]
                    data[i_one[1]] = self.dicts[i_one[0]][self.dicts['nu']][1]
                elif i_one[0]=='tel' and i_one[1]=='telephone':
                    data[i_one[1]]=self.create_tel()
                    self.dicts['sign_in_telephone']=data[i_one[1]]
                else:

                    data[i_one[1]] = self.dicts[i_one[0]]

    def updata_data_Fields_2(self,data,aa,updata_data):
        """
        更新CVS文件data字段
        先从全局字典取值，再更新全局字典;若需要取多个参数/更新多个参数以，隔开（）
        一：2;('userId','user'),('id','shoppcartId')//格式参考 0,1
        二：2;('userId','user'),(('data','id'),'userbankId') // ('data','id')为匹配json类型字段
        三：2;('sign_in_telephone','telephone'),[('id','sign_in_userId'),('token','sign_in_tokenID')] //需要多个全局字典的值

        :param data: 文件请求数据
        :param aa: 全局字典goodsId下标
        :return:
        """
        for i in updata_data:
            i_one = tuple(eval(i))[0]
            # print(i_one)
            if i_one[0] == 'goodsId' and i_one[1] != 'skuId':
                data[i_one[1]] = self.dicts[i_one[0]][aa][0]
            elif i_one[0] == 'goodsId' and i_one[1] == 'skuId':
                data[i_one[0]] = self.dicts[i_one[0]][self.dicts['nu']][0]
                data[i_one[1]] = self.dicts[i_one[0]][self.dicts['nu']][1]
            else:
                data[i_one[1]] = self.dicts[i_one[0]]

    def updata_data_Fields_2_updata_dicts(self,case,data,aa,updata_data):
        """
        更新响应字段
        先从全局字典取值，再更新全局字典;若需要取多个参数/更新多个参数以，隔开（）
        一：2;('userId','user'),('id','shoppcartId')//格式参考 0,1
        二：2;('userId','user'),(('data','id'),'userbankId') // ('data','id')为匹配json类型字段
        三：2;('sign_in_telephone','telephone'),[('id','sign_in_userId'),('token','sign_in_tokenID')] //需要多个全局字典的值

        :param case:对象
        :param data:响应
        :param aa:全局字典goodsId下标
        :return:
        """
        for i in updata_data:
            i_one = tuple(eval(i))[1]
            if isinstance(i_one, list):
                for i_one in i_one:
                    self.updata_data_Fields_2_updata_dicts_1(i_one, case, data, aa)
            else:
                self.updata_data_Fields_2_updata_dicts_1(i_one,case,data,aa)

    def updata_data_Fields_2_updata_dicts_1(self,i_one,case,data,aa):
        a=0
        if i_one[1] in self.dicts.keys():  ###需要更新的字段已经存在在全局字典中
            for j in range(len(self.goods)):  ###防止放入重复的数据
                for q in range(len(self.goods[j])):
                    if case.find_update_data(i_one[0], data) not in self.goods[j][q]:
                        a = 1
            if a == 1 and i_one[0] == 'skuId':
                self.dicts[i_one[1]][aa].append(case.find_update_data(i_one[0], data))
                self.dicts['nu'] = aa
            elif i_one[1] == 'userbankId':
                self.dicts[i_one[1]] = case.find_update_data(i_one[0], data, n=1, keys='userbankId')
            elif a == 1 and i_one[0] != 'skuId':
                self.goods.append(case.set_list(case.find_update_data(i_one[0], data)))
            else:
                self.dicts[i_one[1]] = self.goods
        else:
            if i_one[1] == 'goodsId':
                self.goods.append(case.set_list(case.find_update_data(i_one[0], data)))
                self.dicts[i_one[1]] = self.goods
            elif i_one[1] == 'adrId':
                self.dicts[i_one[1]] = case.find_update_data(i_one[0], data, keys='adrId')
            elif i_one[1] == 'userbankId':
                self.dicts[i_one[1]] = case.find_update_data(i_one[0], data, n=1, keys='userbankId')
            else:
                self.dicts[i_one[1]] = case.find_update_data(i_one[0], data)

    def updata_IN_dicts_value(self,case,data,updata_data):
        """
        更新全局字典已经存在key的值
        3;('userId','user'),('id','shoppcartId')  //  先从全局字典取值，再更新已经在全局字典存在的KEY值

        :param case: case对象
        :param data: 响应数据
        :return:
        """
        for i in updata_data:
            i_one = tuple(eval(i))[1]
            if i_one[1] in self.dicts.keys():  ###需要更新的字段已经存在在全局字典中
                self.dicts[i_one[1]] = case.find_update_data(i_one[0], data)
            else:
                pass

    def updata_data_Fields_4(self,case,data,updata_data):
        """
        随机读取全局字典对应key的值，对象是一个字典
        4;(('userbankId','id')
        :param case: 对象
        :param data: 文件data
        :return:
        """
        for i in updata_data:
            i_one = tuple(eval(i))
            if i_one[0] == 'userbankId':
                list_1 = ['bank-bankId', 'ali-bankId']
                j = random.randint(0, len(list_1) - 1)
                data[i_one[1]] = self.dicts[i_one[0]][0][list_1[j]]
            else:
                data[i_one[1]] = 'null'

    def updata_data_Fields_5(self,case,data,updata_data):
        """
        需要先修改data字段的值，再将修改data的KEY值写进全局字典
        5;('telephone','sign_in_telephone')

        :param case:
        :param data:
        :return:
        """
        for i in updata_data:
            i_one = tuple(eval(i))
            if i_one[0] == 'telephone':
                tel = ''
                for i in range(8):
                    tel += str(random.randint(0, 9))
                data[i_one[0]] = self.create_tel()
                self.dicts[i_one[1]] = data[i_one[0]]

    def create_tel(self):
        """
        随机生成10位数字
        :return:
        """
        tel = '1'
        for i in range(10):
            tel += str(random.randint(0, 9))
        return tel







