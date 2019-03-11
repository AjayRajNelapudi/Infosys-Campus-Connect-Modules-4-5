import pymysql
import os

if os.name == 'nt':
    separator = '\\'
else:
    separator = '/'

class Bank_Database():
    def __init__(self):
        self.database = pymysql.connect("localhost", "root", "anitscse034")
        self.database.autocommit(True)
        self.conn = self.database.cursor()
        self.conn.execute('USE Bank')

    def validate_login(self, c_id, password):
