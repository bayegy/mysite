import numpy as np
import pandas as pd
import pymysql
import re


class Mysql(object):
    """connector of mysql"""

    def __init__(self, host, user, passwd, db):
        self._db = pymysql.connect(host, user, passwd, db)
        self.cursor = self._db.cursor()
        self.pd = pd
        self.pd.set_option('max_colwidth', 1000)

    def __insert_sql__(self, table_name, field_name_list, value_list) -> str:
        value_list = [i if (i or i == 0) else np.nan for i in value_list]
        return "insert into `{}` {} values {};".format(table_name, str(tuple(field_name_list)).replace("'", "`"), str(tuple(value_list)).replace("nan", "null"))

    def commit(self, sql=None):
        try:
            if sql:
                self.cursor.execute(sql)
            self._db.commit()
        except Exception as e:
            print(e)
            self._db.rollback()

    def fetchall(self) -> tuple:
        return self.cursor.fetchall()

    def get_field_name(self, table_name) -> []:
        sql = "select COLUMN_NAME from information_schema.COLUMNS where table_name = '{}'".format(table_name)
        self.commit(sql)
        return [tp[0] for tp in self.fetchall()].remove('索引')

    def create_table(self, table_name, field_name_list, type_list, primary_key=None):
        sqlhead = "CREATE TABLE IF NOT EXISTS `{}`(".format(table_name)
        sqltail = ")ENGINE=InnoDB DEFAULT CHARSET=utf8;"
        sqlbody = '`索引` INT UNSIGNED AUTO_INCREMENT,'
        for nm, tp in zip(field_name_list, type_list):
            sqlbody = sqlbody + '`' + nm + '`' + ' ' + tp + ','
        key = primary_key if primary_key else '索引'
        sqlbody = sqlbody + "PRIMARY KEY ( `{}` )".format(key)
        sql = sqlhead + sqlbody + sqltail
        self.commit(sql)

    def table_exists(self, table_name) -> bool:
        """check if the mysql table exists"""
        sql = "show tables;"
        self.cursor.execute(sql)
        tables = [self.cursor.fetchall()]
        table_list = re.findall('(\'.*?\')', str(tables))
        table_list = [re.sub("'", '', each) for each in table_list]
        if table_name in table_list:
            return True
        else:
            return False

    def nptype_to_sqltype(self, nptype) -> str:
        if nptype == np.dtype('int64'):
            return 'INT'
        elif nptype == np.dtype('float64'):
            return 'DOUBLE'
        else:
            return 'VARCHAR(1000)'

    def insert(self, table_name, records, field_name_list=None):
        shape_jg = np.array(records)
        field_name_list = field_name_list if field_name_list else self.get_field_name(table_name)
        try:
            shape_jg.shape[1]
            for value_list in records:
                sql = self.__insert_sql__(table_name, field_name_list, value_list)
                self.cursor.execute(sql)
            self.commit()
        except Exception:
            self.commit(self.__insert_sql__(table_name, field_name_list, records))

    def read_csv(self, path, table_name, sep="\t", primary_key=None):
        df = self.pd.read_csv(path, sep=sep)
        field_name_list = list(df.columns)
        if not self.table_exists(table_name):
            type_list = [self.nptype_to_sqltype(dt) for dt in list(df.dtypes.values)]
            self.create_table(table_name, field_name_list, type_list, primary_key)
        self.insert(table_name, df.values, field_name_list)

    def select(self, table_name, field="*", condition=None) -> pd.DataFrame:
        """Remember to use `` when encounter some special field name. e.g. `IF` """
        field = [field] if isinstance(field, str) else field
        field = ','.join(['%s'] * len(field)) % tuple(field)
        condition = "where " + condition if condition else ""
        sql = "select {} from {} {};".format(field, table_name, condition)
        self.cursor.execute(sql)
        dt = self.cursor.fetchall()
        columns = [tp[0] for tp in self.cursor.description]
        return self.pd.DataFrame(np.array(dt), columns=columns)

    def close(self):
        self._db.close()
