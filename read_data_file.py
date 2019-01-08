#-*- coding:utf-8 -*-
import codecs
import csv
import json

import xlrd


def get_all_data():
    """
    获取所有数据
    :return:
    """
    cases = dict()
    sheet_data = []
    excel = xlrd.open_workbook("../datafile/data_file_01.xls")
    for sheet in excel.sheets():
        for n in range(2, sheet.nrows):
            sheet_data.append(dict(zip(sheet.row_values(1), sheet.row_values(n))))
        cases[sheet.name] = sheet_data
    return cases

class Readfile():




    def get_data(self,data):
        """
        转换数据格式
        :param data:
        :return:
        """
        d = {}
        for param in data.split('&'):
            k, v = param.split('=')
            d.update(k=v)
        return d

    # def read_url(self,i):
    #     with open("../datafile/data_file.csv","r") as csvfile:
    #         # 读取csv文件，返回的是迭代类型
    #         read = csv.DictReader(csvfile)
    #         #返回Url列的所有数据
    #         url = [row['Url'] for row in read]
    #     return url[i]
    #
    # def read_data(self,i):
    #     with open("../datafile/data_file.csv","r") as csvfile:
    #         # 读取csv文件，返回的是迭代类型
    #         read = csv.DictReader(csvfile)
    #         # 返回Data列的所有数据
    #         data = [row['Data'] for row in read]
    #     return self.get_data(data[i])
    #
    # def read_headers(self,i):
    #     with open("../datafile/data_file.csv","r") as csvfile:
    #         # 读取csv文件，返回的是迭代类型
    #         read = csv.DictReader(csvfile)
    #         header = [row['headers'] for row in read]
    #         print(header[i])
    #     return header[i]
    #
    # def read_params(self,i):
    #     with open("../datafile/data_file.csv","r") as csvfile:
    #         # 读取csv文件，返回的是迭代类型
    #         read = csv.DictReader(csvfile)
    #         #返回Params列的所有数据
    #         params = [row['Params'] for row in read]
    #     return params[i]
    #
    # def read_code(self,i):
    #     with open("../datafile/data_file.csv","r") as csvfile:
    #         # 读取csv文件，返回的是迭代类型
    #         read = csv.DictReader(csvfile)
    #         #返回Params列的所有数据
    #         Code = [row['Code'] for row in read]
    #     return Code[i]
    #
    # def read_title(self,i):
    #     with open("../datafile/data_file.csv","r") as csvfile:
    #         # 读取csv文件，返回的是迭代类型
    #         read = csv.DictReader(csvfile)
    #         #返回Params列的所有数据
    #         title = [row['title'] for row in read]
    #     return title[i]
    #
    # def read_success(self, i):
    #     with open("../datafile/data_file.csv", "r") as csvfile:
    #         # 读取csv文件，返回的是迭代类型
    #         read = csv.DictReader(csvfile)
    #         # 返回Params列的所有数据
    #         success = [row['success'] for row in read]
    #     return bool((success[i]))###返回bool类型
    #
    # def read_lenth(self):
    #     with open("../datafile/data_file.csv","r") as csvfile:
    #         # 读取csv文件，返回的是迭代类型
    #         read = csv.DictReader(csvfile)
    #         #返回Params列的所有数据
    #         lenth = [row['title'] for row in read]
    #     return len(lenth)
    #
    #
    # def read_sql_condit(self,i):
    #     with open("../datafile/data_file.csv","r") as csvfile:
    #         # 读取csv文件，返回的是迭代类型
    #         read = csv.DictReader(csvfile)
    #         #返回Params列的所有数据
    #         sql_condit = [row['title'] for row in read]
    #     return sql_condit[i]
    #
    # def read_sql_Table(self,i):
    #     with open("../datafile/data_file.csv","r") as csvfile:
    #         # 读取csv文件，返回的是迭代类型
    #         read = csv.DictReader(csvfile)
    #         #返回Params列的所有数据
    #         sql_Table = [row['title'] for row in read]
    #     return sql_Table[i]