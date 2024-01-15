import pymysql
import datetime

import pymysql
import configparser

conf = configparser.ConfigParser()
conf.read('conf/dataBase.conf', encoding='gbk')
host = conf.get("mysql", 'host')
user = conf.get("mysql", 'user')
password = conf.get("mysql", 'password')
db = conf.get("mysql", 'db')
port = int(conf.get("mysql", 'port'))
charset = conf.get("mysql", 'charset')

class DbOperate():

    def __init__(self):
        self.conn=pymysql.connect(
                        host=host,
                        user=user,
                        password=password,
                        db=db,
                        port=port,
                        charset=charset
                               )

    #先注释掉吧，逻辑不一样。。。重新整没时间了。。。。
    def execute_with_bool(self, sql_str, args=()):
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql_str, args)
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print(e)
            return False
        finally:
            cursor.close()



#返回全体人员信息
    def get_all_user(self):

        cur = self.conn.cursor()
        try:
            cur.execute('SELECT * FROM employee')
            result = cur.fetchall()
            print("result:", result)
        except Exception as e:
            print(e)

        cur.close()
        return result

    def user_identity(self, index):
        sql_str = "SELECT * FROM employee WHERE employee.ID=" + str(index)
        cur = self.conn.cursor()
        try:
            result = cur.execute(sql_str)
            result = cur.fetchall()
            print(result)
        except Exception as e:
            print("error",e)

        cur.close()
        return result

#插入用户签到数据
    def register_date(self, id, name, tt):
        cur = self.conn.cursor()
        sql = "INSERT INTO record(id, name, date) VALUES(%d, '%s','%s');" % (id,
                name, tt)
        try:
            cur.execute(sql)
            self.conn.commit()
            print("you have successfully inserted data!")
        except Exception as e:
            print(e)
            self.conn.rollback()
        cur.close()

#返回表table_name的个数
    def list_sum(self, table_name):
        cur = self.conn.cursor()
        sql = "SELECT COUNT(*) FROM " + table_name
        try:
            cur.execute(sql)
            self.conn.commit()
            result = cur.fetchall()
            print(result[0][0])
        except Exception as e:
            print(e)
        cur.close()
        return result[0][0]

#返回单个用户的全部签到日期，用于判定是否已经签到
    def return_date(self, name):
        cur = self.conn.cursor()
        sql = "SELECT date FROM record WHERE record.name='cxp';"
        try:
            self.cur.execute(sql)
            res = self.cur.fetchall()
            print(res[1][0])
            print(type(res[1][0]))
        except Exception as e:
            print(e)
        cur.close()

#删除雇员
    def delete_employee(self, index):
        cur = self.conn.cursor()
        sql = "DELETE FROM employee WHERE employee.ID=" + index
        try:
            cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
            cur.close()
            return 1

#添加雇员
    def add_employee(self, index, name):
        cur = self.conn.cursor()
        sql = "INSERT INTO employee(ID, name) VALUES(%d, '%s');" % (index,
                                                                    name)
        try:
            cur.execute(sql)
            self.conn.commit()
            print("you have successfully inserted data!")
        except Exception as e:
            print(e)
            self.conn.rollback()
            cur.close()
            return 1
        cur.close()

    #额。。。。。。。。
    def close_connection(self):
        self.conn.close()



