import pymysql
import os
import idgen

if os.name == 'nt':
    separator = '\\'
else:
    separator = '/'

class Bank_Database():
    def __init__(self):
        self.database = pymysql.connect("localhost", "root", "anitscse034")
        self.conn = self.database.cursor()
        self.conn.execute('USE Bank')
        self.id_gen = idgen.Id_Generator()

    def create_account(self, name, addr, password, account_type, account_balance):
        try:
            c_id = self.id_gen.generate_customer_id()
            acc_no = self.id_gen.generate_account_no()

            customer_insert_query = "INSERT INTO Customer VALUES (%s, '%s', '%s', '%s')" % (c_id, password, name, addr)
            self.conn.execute(customer_insert_query)

            account_insert_query = "INSERT INTO Account VALUES (%s, %s, '%s')" % (acc_no, account_balance, account_type)
            self.conn.execute(account_insert_query)

            customer_account_insert_query = "INSERT INTO CustomerAccount VALUES (%s, %s)" % (c_id, acc_no)
            self.conn.execute(customer_account_insert_query)

            self.database.commit()
            return (c_id, acc_no)
        except:
            return (None, None)

    def validate_login(self, c_id, password):
        query = "SELECT * FROM Customer WHERE c_id = %s AND c_password = '%s'" % (c_id, password)
        if self.conn.execute(query) == 1:
            return True
        return False

    def change_address(self, c_id, new_addr):
        query = "UPDATE Customer SET addr = '%s' WHERE c_id = %s" % (new_addr, c_id)
        self.database.commit()
        self.conn.execute(query)

    def deposit_money(self, acc_no, money):
        try:
            deposit_query = "UPDATE Account SET acc_balance = acc_balance + %s WHERE acc_no = %s" % (money, acc_no)
            transaction_log_query = "INSERT INTO AccountTransaction VALUES (%s, 'deposit', %s, NOW())" % (acc_no, money)
            self.conn.execute(deposit_query)
            self.conn.execute(transaction_log_query)

            self.database.commit()
            return True
        except:
            return False

    def withdraw_money(self, acc_no, money):
        try:
            enquire_balance_query = "SELECT acc_balance FROM Account WHERE acc_no = %s" % (acc_no)
            self.conn.execute(enquire_balance_query)
            acc_balance = self.conn.fetchone()[0]
            if acc_balance - money > 500:
                acc_balance = acc_balance - money
            else:
                return False

            withdraw_query = "UPDATE Account SET acc_balance = %s WHERE acc_no = %s" % (acc_balance, acc_no)
            self.conn.execute(withdraw_query)

            transaction_log_query = "INSERT INTO AccountTransaction VALUES (%s, 'withdrawl', %s, NOW())" % (acc_no, money)
            self.conn.execute(transaction_log_query)

            self.database.commit()
            return True
        except:
            return False

bank_db = Bank_Database()
c_id, acc_no = bank_db.create_account('Ajay', 'seethamadhara', 'anitscse034', 'current', '100000000')
bank_db.deposit_money(acc_no, 1000)
bank_db.withdraw_money(acc_no, 1000)
