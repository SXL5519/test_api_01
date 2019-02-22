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

