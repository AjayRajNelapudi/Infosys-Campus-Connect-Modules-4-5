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

    def validate_admin_login(self, admin_id, admin_password):
        query = "SELECT * FROM Administrator WHERE admin_id = %s AND admin_password = '%s'" % (admin_id, admin_password)
        if self.conn.execute(query) == 1:
            return True
        return False

    def change_address(self, c_id, new_addr):
        try:
            query = "UPDATE Customer SET c_addr = '%s' WHERE c_id = %s" % (new_addr, c_id)
            self.conn.execute(query)

            self.database.commit()
            return True
        except:
            return False

    def deposit_money(self, acc_no, amount, commit_on_success=True):
        try:
            deposit_query = "UPDATE Account SET acc_balance = acc_balance + %s WHERE acc_no = %s" % (amount, acc_no)
            transaction_log_query = "INSERT INTO AccountTransaction VALUES (%s, 'deposit', %s, NOW())" % (acc_no, amount)
            self.conn.execute(deposit_query)
            self.conn.execute(transaction_log_query)

            if commit_on_success:
                self.database.commit()
            return True
        except:
            return False

    def withdraw_money(self, acc_no, amount, commit_on_success=True):
        try:
            enquire_balance_query = "SELECT acc_balance FROM Account WHERE acc_no = %s" % (acc_no)
            self.conn.execute(enquire_balance_query)
            acc_balance = self.conn.fetchone()[0]
            if acc_balance - int(amount) > 500:
                acc_balance = acc_balance - int(amount)
            else:
                return False

            withdraw_query = "UPDATE Account SET acc_balance = %s WHERE acc_no = %s" % (acc_balance, acc_no)
            self.conn.execute(withdraw_query)

            transaction_log_query = "INSERT INTO AccountTransaction VALUES (%s, 'withdrawl', %s, NOW())" % (acc_no, amount)
            self.conn.execute(transaction_log_query)

            if commit_on_success:
                self.database.commit()
            return True
        except:
            self.database.rollback()
            return False

    def transfer_money(self, src_acc_no, dest_acc_no, amount):
        withdraw_status = self.withdraw_money(src_acc_no, amount, commit_on_success=False)
        deposit_status = self.deposit_money(dest_acc_no, amount, commit_on_success=False)

        if withdraw_status and deposit_status:
            self.database.commit()
            return True
        return False

    def get_statement(self, acc_no):
        query = "SELECT * FROM AccountTransaction WHERE acc_no = %s" % (acc_no)
        self.conn.execute(query)
        statement = self.conn.fetchall()
        return statement

    def close_account(self, acc_no):
        try:
            delete_customer_account_query = "DELETE FROM CustomerAccount WHERE acc_no = %s" % (acc_no)
            self.conn.execute(delete_customer_account_query)

            #delete_account_query = "DELETE FROM Account WHERE acc_no = %s" % (acc_no)
            #self.conn.execute(delete_account_query)

            insert_closed_account_query = "INSERT INTO ClosedAccount VALUES (%s, NOW())" % (acc_no)
            self.conn.execute(insert_closed_account_query)

            self.database.commit()
            return True
        except:
            self.database.rollback()
            return False

    def is_associated_account(self, c_id, acc_no):
        query = "SELECT * FROM CustomerAccount WHERE c_id = %s AND acc_no = %s" % (c_id, acc_no)
        status = self.conn.execute(query)
        if status == 1:
            return True
        return False

    def get_closed_accounts(self):
        query = '''
                SELECT A.*
                FROM ClosedAccount CA, Account A
                WHERE A.acc_no = CA.acc_no
                ORDER BY CA.closing_date
        '''
        self.conn.execute(query)
        closed_accounts = self.conn.fetchall()
        return closed_accounts