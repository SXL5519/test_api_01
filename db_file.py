import pprint

import pymongo
import pymysql
import readConfig as readConfig
from pymongo import MongoClient


localReadConfig = readConfig.ReadConfig()

class DB:


    def __init__(self):
        # self.log = Log.get_log()
        # self.logger = self.log.get_logger()
        global host, username, password, port, database, mysql_config
        host = localReadConfig.get_db("host")
        username = localReadConfig.get_db("username")
        password = localReadConfig.get_db("password")
        port = int(localReadConfig.get_db("port"))
        database = localReadConfig.get_db("database")
        mysql_config = {
            'host': str(host),
            'user': username,
            'passwd': password,
            'port': int(port),
            'db': database
        }

        # self.db = None
        # self.cursor = None

    def connect_mongodb_all(self,table,n=None):
        """
        查询mongoDB数据
        :param table: 表名
        :param n: 查询条件
        :return:
        """
        client = MongoClient(host=host,port=port)
        db = client[database]
        print(db)
        collection = db[table]
        print(collection)
        print(n)
        value=collection.find_one(n)
        print(value)
        client.close()
        return value

    def connect_mysql_all(self,sql,params):
        """
        查询sql全部数据
        :param sql:
        :param params:
        :return:
        """
        db = pymysql.connect(**mysql_config)
        cursor = self.db.cursor()
        cursor.execute(sql, params)
        db.commit()
        value = cursor.fetchall()
        self.cursor.close()
        self.db.close()
        print("Database closed!")
        return value

    def connect_mysql_one(self,sql,params):
        """
        查询sql一条数据
        :param sql:
        :param params:
        :return:
        """
        db = pymysql.connect(**mysql_config)
        cursor = self.db.cursor()
        cursor.execute(sql, params)
        db.commit()
        value = cursor.fetchone()
        self.cursor.close()
        self.db.close()
        print("Database closed!")
        return value


    def connectDB(self):
        """
        链接数据库
        :return:
        """
        try:
            # connect to DB
            self.db = pymysql.connect(**mysql_config)
            # create cursor  创建游标
            self.cursor = self.db.cursor()
            print("Connect DB successfully!")
        except ConnectionError as ex:
            raise
            # self.logger.error(str(ex))

    def executeSQL(self, sql, params):
        """
        执行sql语句
        :param sql:
        :param params: sql语句的参数
        :return:
        """
        self.connectDB()
        # executing sql
        self.cursor.execute(sql, params)
        # executing by committing to DB
        self.db.commit()
        return self.cursor

    def get_all(self, cursor):
        """
        获取查询的全部数据
        :param cursor:
        :return:
        """
        value = cursor.fetchall()
        return value

    def get_one(self, cursor):
        """
        获取查询出的一条数据
        :param cursor:
        :return:
        """
        value = cursor.fetchone()
        return value

    def closeDB(self):
        """
        关闭数据库
        :return:
        """
        self.cursor.close()
        self.db.close()
        print("Database closed!")

