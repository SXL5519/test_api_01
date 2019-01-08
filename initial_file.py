#-*- coding:utf-8 -*-
import unittest
from function import logfile
class MyTest(unittest.TestCase):

    # def setUp(self):
    #     logfile()

    @classmethod
    def setUpClass(cls):
        # logfile()
        pass
    def tearDown(self):
        print("case over")
