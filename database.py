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


    def create_account(self, name, addr, password, account_type, account_balance):
        try:
            c_id = None
            acc_no = None
            customer_insert_query = "INSERT INTO Customer VALUES (%s, '%s', '%s', '%s')" % (c_id, password, name, addr)
            account_insert_query = "INSERT INTO Account VALUES (%s, %s, '%s')" % (acc_no, account_balance, account_type)
            self.conn.execute(customer_insert_query)
            self.conn.execute(account_insert_query)

            return (c_id, acc_no)
        except:
            return (None, None)

    def validate_login(self, c_id, password):
        query = "SELECT * FROM Customer WHERE c_id = %s AND c_password = '%s'" % (c_id, password)
        if self.conn.execute(query) == 1:
            return True
        return False

