import numpy as np 
import pandas as pd 
import pymysql

class Mysql(object):
    """connector of mysql"""
    def __init__(self,host,user,passwd,db):
        self._db=pymysql.connect(host,user,passwd,db)
        self.cursor=self._db.cursor()

    def create_table(self,table_name,field_name_list,type_list,primary_key=None):
        sqlhead="CREATE TABLE IF NOT EXISTS `{}`(".format(table_name)
        sqltail=")ENGINE=InnoDB DEFAULT CHARSET=utf8;"
        sqlbody='`索引` INT UNSIGNED AUTO_INCREMENT,'
        for nm,tp in zip(field_name_list,type_list):
            sqlbody = sqlbody + '`' + nm + '`' + ' ' + tp + ','
        key = primary_key if primary_key else '索引'
        sqlbody = sqlbody + "PRIMARY KEY ( `{}` )".format(key)
        sql = sqlhead + sqlbody + sqltail
        self.cursor(sql)
