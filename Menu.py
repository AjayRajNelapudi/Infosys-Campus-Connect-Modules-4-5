import database

class MainMenu:
    def __init__(self):
        self.bank_db = database.Bank_Database()
        self.c_id = -1

    def display_main_menu(self):
        print("Enter Your Service")
        print("1. Sign Up")
        print("2. Sign In")
        print("3. Admin Sign In")
        print("4. Quit")

        choice = int(input("Enter your choice: "))
        return choice

    def perform_menu_action(self, action):
        if action == 1:
            name, addr, password, account_type, account_balance = self.sign_up()
            c_id, acc_no = self.bank_db.create_account(name, addr, password, account_type, account_balance)
            if c_id == None or acc_no == None:
                print("Failed")
            else:
                print("c_id", c_id)
                print("acc_no", acc_no)
        elif action == 2:
            if not self.prompt_customer_login():
                print("Account Locked")
            else:
                result = self.sign_in()
                self.perform_customer_action(result)
        elif action == 3:
            if not self.prompt_admin_login():
                print("Login Failed")
            else:
                result = self.admin_sign_in()
                self.perform_admin_action(result)
        elif action == 4:
            exit()
        else:
            print("Enter proper choice")

    def sign_up(self):
        name = input("Enter your name: ")
        password = input("Enter password: ")
        addr = input("Enter your address: ")
        account_balance = input("Enter amount to deposit: ")
        account_type = input("Enter account type (CA / SA / FD): ")

        return (name, addr, password, account_type, account_balance)

    def prompt_customer_login(self):
        for i in range(3):
            c_id = input("Enter customer id: ")
            password = input("Enter password: ")

            if self.bank_db.validate_login(c_id, password):
                self.c_id = c_id
                return True
            else:
                print(3 - (i + 1), 'attempts left')
        else:
            return False

    def sign_in(self):
        print("Select Customer Service")
        print("1. Address Change")
        print("2. Create Account")
        print("3. Money Deposit")
        print("4. Money Widthdrawal")
        print("5. Print Statement")
        print("6. Transfer Money")
        print("7. Account Closure")
        print("8. Avail Loan")
        print("9. Logout")

        choice = int(input())
        return choice

    def perform_customer_action(self, action):
        while True:
            if action == 1:
                new_addr = input("Enter new address: ")
                if self.bank_db.change_address(self.c_id, new_addr):
                    print("Success")
                else:
                    print("Failed")
            elif action == 2:
                print("1. Open Savings Account")
                print("2. Open Current Account")
                print("3. Open Fixed Deposit Account")

                choice = int(input("Enter your choice: "))

                accounts = {1: "SA", 2: "CA", 3: "FD"}
                account_type = accounts[choice]

                accont_balance = input("Enter amount: ")

                acc_no = self.bank_db.open_account(self.c_id, account_type, accont_balance)
                if acc_no:
                    print("Success")
                    print("Account No:", acc_no)
                else:
                    print("Failed")

            elif action == 3:
                acc_no = input("Enter account no: ")

                if not self.bank_db.is_associated_account(self.c_id, acc_no):
                    print("Not associated account")
                    continue

                amount = input("Enter amount: ")
                if self.bank_db.deposit_money(acc_no, amount):
                    print("Success")
                else:
                    print("Failed")
            elif action == 4:
                acc_no = input("Enter account no: ")

                if not self.bank_db.is_associated_account(self.c_id, acc_no):
                    print("Not associated account")
                    continue

                amount = input("Enter amount: ")
                if self.bank_db.withdraw_money(acc_no, amount):
                    print("Success")
                else:
                    print("Failed")
            elif action == 5:
                acc_no = input("Enter account no: ")

                if not self.bank_db.is_associated_account(self.c_id, acc_no):
                    print("Not associated account")
                    continue

                statement = self.bank_db.get_statement(acc_no)
                print(statement)
            elif action == 6:
                src_acc = input("Enter source account no: ")

                if not self.bank_db.is_associated_account(self.c_id, src_acc):
                    print("Not associated account")
                    continue

                dest_acc = input("Enter destination account no: ")
                amount = input("Enter amount to transfer: ")
                if self.bank_db.transfer_money(src_acc, dest_acc, amount):
                    print("Success")
                else:
                    print("Failed")
            elif action == 7:
                acc_no = input("Enter account no: ")

                if not self.bank_db.is_associated_account(self.c_id, acc_no):
                    print("Not associated account")
                    continue

                if self.bank_db.close_account(acc_no):
                    print("Success")
                else:
                    print("Failed")
            elif action == 8:
                acc_no = input("Enter account no: ")

                if not self.bank_db.is_associated_account(self.c_id, acc_no):
                    print("Not associated account")
                    continue

                loan_amount = input("Enter loan amount: ")

                loan_sanctioned = self.bank_db.avail_loan(acc_no, loan_amount)
                if loan_sanctioned:
                    print("Success")
                else:
                    print("Failed")
            elif action == 9:
                self.logout()
                print("Logged Out")
                break

            action = int(input("Enter your choice: "))

    def prompt_admin_login(self):
        admin_id = input("Enter admin id: ")
        admin_password = input("Enter admin password: ")

        return self.bank_db.validate_admin_login(admin_id, admin_password)

    def admin_sign_in(self):
        print("Select Admin Service")
        print("1. Print Closure Account History")
        print("2. FD Report of a customer")
        print("3. FD Report of Customers vis-à-vis another Customer")
        print("4. FD Report of Customers w.r.t a particular FD Amount")
        print("5. Loan Report of a Customer")
        print("6. Loan Report of Customers vis-à-vis another Customer")
        print("7. Loan Report of Customers w.r.t a particular Loan Amount")
        print("8. Loan – FD Report of Customers")
        print("9. Report of Customers who are yet to avail a loan (customer id, first name, last name)")
        print("10. Report of Customers who are yet to open a FD account (customer id, first name, last name)")
        print("11. Report of Customers who neither have a loan nor a FD account with the bank (customer id, first name, last name)")
        print("0. Admin Logout")

        choice = int(input())
        return choice

    def perform_admin_action(self, action):
        while True:
            if action == 1:
                report = self.bank_db.get_closed_accounts()
                print(report)
            elif action == 2:
                c_id = input("Enter c_id: ")
                report = self.bank_db.get_fd_report(c_id)
                print(report)
            elif action == 3:
                c_id = input("Enter c_id: ")
                report = self.bank_db.get_fd_report_vis_a_vis_customer(c_id)
                print(report)
            elif action == 4:
                amount = input("Enter amount: ")
                report = self.bank_db.get_fd_report_wrt_amount(amount)
                print(report)
            elif action == 5:
                c_id = input("Enter c_id: ")
                report = self.bank_db.get_loan_report_of_customer(c_id)
                print(report)
            elif action == 6:
                c_id = input("Enter c_id: ")
                report = self.bank_db.get_fd_report_vis_a_vis_customer(c_id)
                print(report)
            elif action == 7:
                amount = input("Enter amount: ")
                report = self.bank_db.get_loan_report_wrt_amount(amount)
                print(report)
            elif action == 8:
                report = self.bank_db.get_loan_fd_report()
                print(report)
            elif action == 9:
                report = self.bank_db.get_no_loan_customers()
                print(report)
            elif action == 10:
                report = self.bank_db.get_no_fd_acc_customers()
                print(report)
            elif action == 11:
                report = self.bank_db.get_no_loan_no_fd_customers()
                print(report)
            elif action == 0:
                break

            action = int(input("Enter your choice: "))

    def logout(self):
        self.c_id = -1


menu = MainMenu()
while True:
    choice = menu.display_main_menu()
    menu.perform_menu_action(choice)