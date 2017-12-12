import json
import sqlite3

class data_conn:
    def __init__(self):
        with open('json/base_info.json') as json_file:
            base_data = json.load(json_file)

        self.db_name = base_data['database']
        self.conn = None

    def start(self):
        self.conn = sqlite3.connect('db/' + self.db_name)
        pass

    def end(self):
        self.conn.close()
        pass