import pymysql
import json

class data_conn:
    def __init__(self):
        with open('base_info.json') as json_file:
            base_data = json.load(json_file)
        db_data = base_data['database']
        self.hostname = db_data['db_hostname']
        self.username = db_data['db_username']
        self.passwd = db_data['db_passwd']
        self.select_database = db_data['db_select_database']
        self.conn = None

    def start(self):
        self.conn = pymysql.connect(host = self.hostname,port=3306,user = self.username, password = self.passwd,
                                    db = self.select_database,charset='utf8')
        pass

    def end(self):
        self.conn.close()
        pass