import random

class Id_Generator():
    def __init__(self):
        self.customer_id = random.randint(1, 1000)
        self.account_no = random.randint(1, 1000000000)
        self.loan_id = random.randint(1, 10000)

    def generate_customer_id(self):
        self.customer_id += 1
        return self.customer_id

    def generate_account_no(self):
        self.account_no += 1
        return self.account_no

    def generate_loan_id(self):
        self.loan_id += 1
        return self.loan_id
