import json
import os
import getpass
from colorama import init, Fore, Style

init(autoreset=True)

DATA_FILE = 'users.json'

class User:
    def __init__(self, pin, balance=0, history=None):
        self.pin = pin
        self.balance = balance
        self.history = history or []

    def deposit(self, amount):
        if amount <= 0:
            print(Fore.RED + "Amount must be positive.")
            return
        self.balance += amount
        self.history.append(f"Deposited ₹{amount}")
        print(Fore.GREEN + f"₹{amount} deposited successfully.")

    def withdraw(self, amount):
        if amount <= 0:
            print(Fore.RED + "Amount must be positive.")
            return
        if amount > self.balance:
            print(Fore.RED + "Insufficient balance.")
            return
        self.balance -= amount
        self.history.append(f"Withdrew ₹{amount}")
        print(Fore.GREEN + f"₹{amount} withdrawn successfully.")

    def show_balance(self):
        print(Fore.BLUE + f"Your current balance: ₹{self.balance}")

    def show_history(self):
        print(Fore.CYAN + "\nTransaction History:")
        if not self.history:
            print("No transactions yet.")
        else:
            for h in self.history:
                print(f" - {h}")

class ATM:
    def __init__(self):
        self.users = self.load_data()

    def load_data(self):
        if not os.path.exists(DATA_FILE):
            return {}
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
            return {uid: User(**info) for uid, info in data.items()}

    def save_data(self):
        data = {uid: vars(user) for uid, user in self.users.items()}
        with open(DATA_FILE, 'w') as file:
            json.dump(data, file, indent=2)

    def create_account(self):
        uid = input(Fore.BLUE + "Choose a User ID: ").strip()
        if uid in self.users:
            print(Fore.RED + "User ID already exists.")
            return
        pin = getpass.getpass("Set a 4-digit PIN: ").strip()
        if len(pin) != 4 or not pin.isdigit():
            print(Fore.RED + "PIN must be exactly 4 digits.")
            return
        self.users[uid] = User(pin)
        self.save_data()
        print(Fore.GREEN + "Account created successfully.")

    def login(self):
        uid = input(Fore.BLUE + "Enter your User ID: ").strip()
        pin = getpass.getpass("Enter your PIN: ").strip()
        user = self.users.get(uid)
        if not user or user.pin != pin:
            print(Fore.RED + "Invalid credentials.")
            return
        print(Fore.GREEN + f"\nWelcome, {uid}!\n")
        self.user_menu(user)
        self.save_data()

    def user_menu(self, user):
        while True:
            print(Fore.MAGENTA + "\n--- ATM Menu ---")
            print("1. Check Balance")
            print("2. Deposit")
            print("3. Withdraw")
            print("4. Transaction History")
            print("5. Logout")
            choice = input(Fore.BLUE + "Choose an option: ").strip()

            if choice == '1':
                user.show_balance()
            elif choice == '2':
                try:
                    amt = float(input("Enter amount to deposit: "))
                    user.deposit(amt)
                except ValueError:
                    print(Fore.RED + "Invalid amount.")
            elif choice == '3':
                try:
                    amt = float(input("Enter amount to withdraw: "))
                    user.withdraw(amt)
                except ValueError:
                    print(Fore.RED + "Invalid amount.")
            elif choice == '4':
                user.show_history()
            elif choice == '5':
                print(Fore.GREEN + "Logging out...\n")
                break
            else:
                print(Fore.RED + "Invalid choice. Try again.")

    def main_menu(self):
        print(Fore.CYAN + Style.BRIGHT + "\n========= Welcome to Smart ATM =========")
        while True:
            print(Fore.MAGENTA + "\n--- Main Menu ---")
            print("1. Login")
            print("2. Create Account")
            print("3. Exit")
            choice = input(Fore.BLUE + "Select an option: ").strip()

            if choice == '1':
                self.login()
            elif choice == '2':
                self.create_account()
            elif choice == '3':
                print(Fore.GREEN + "Thank you for using the ATM. Goodbye!")
                break
            else:
                print(Fore.RED + "Invalid option. Try again.")

if __name__ == "__main__":
    atm = ATM()
    atm.main_menu()
