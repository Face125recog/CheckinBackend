# -*- coding: utf-8 -*-
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


def init_conn():
    conn = pymysql.connect(
        host=host,  # 数据库的IP地址
        user=user,  # 数据库用户名称
        password=password,  # 数据库用户密码
        db=db,  # 数据库名称
        port=port,  # 数据库端口名称
        charset=charset  # 数据库的编码方式
    )
    return conn

#没放上去databaseOp.py....
def execute_with_bool(sql_str, args=()):
    conn = init_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(sql_str, args)
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(e)
        return False
    finally:
        cursor.close()


def create_table_employee():
    return execute_with_bool('''
        CREATE TABLE IF NOT EXISTS `''' + db + '''`.`employee`  (
        ID INT PRIMARY KEY AUTO_INCREMENT,
      `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL ) 
''')

# #创建记录表,反正没有用，先注释掉吧
# def create_table_record():
#     return execute_with_bool('''
#         CREATE TABLE IF NOT EXISTS `''' + db + '''`.`record`  (
#         ID INT PRIMARY KEY AUTO_INCREMENT,
#       `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL )
# ''')


if __name__ == '__main__':
    create_table_employee()