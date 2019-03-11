# Shivm's Code goes here
import string


class MainMenu:
    def display_main_menu(self):
        print("Enter Your Service")
        print("1. Sign Up")
        print("2. Sign In")
        print("3. Admin Sign In")
        print("4. Quit")

        option = int(input())
        return option

    def sign_up(self):
        result = {}

        print("Enter Your Name")
        result["name"] = input()
        print("Enter Your Password")
        result["password"] = input()
        print("Enter Your Address")
        result["addr"] = input()
        print("Enter The Amount To Deposite")
        result["balance"] = int(input())
        print("Enter Account Type You Want To Open")
        result["account_type"] = input()
        return result

    def sign_in(self):
        result = {}

        print("Enter your Coustomer ID")
        result["c_id"] = int(input())
        print("Enter Your Password")
        result["password"] = input()
        print("Select Customer Service")
        print("1. Address Change")
        print("2. Money Deposite")
        print("3. Money Widthdrawal")
        print("4 Print Statement")
        print("5.Transfer Money")
        print("6.Account Closure")
        print("7.Logout")
        result["signin_option"] = int(input())
        return result

    def admin_sign_in(self):
        result = {}
        print("Enter Admin ID")
        result["admin_id"] = int(input())
        print("Enter Admin Password")
        result["admin_password"] = input()
        print("Select Admin Service")
        print("1. Print Closure Account  History")
        print("2. Admin Logout")
        result["admin_option"] = int(input())
        return result


menu = MainMenu()
while True:
    choice = menu.display_main_menu()
    if choice == 1:
        result = menu.sign_up()
        print(result)
    elif choice == 2:
        result = menu.sign_in()
        print(result)
    elif choice == 3:
        result = menu.admin_sign_in()
        print(result)
    else:
        exit()