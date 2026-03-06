import json
import os

basedir = os.path.dirname(os.path.abspath(__file__))
UserInfoFile = os.path.join(basedir, "UsersInfo.json")

users_info = {}

with open(UserInfoFile, "r") as file:
    users_info = json.load(file)

def str_ask(prompt):
    while True:
        value = input(prompt)
        if value.strip() == "":
            print("Input cannot be empty. Please try again.")
        else:
            return value

#Methods adds a new user to the users_info dictionary and updates the JSON file
def add_user(name, password) -> bool:
    if name in users_info:
        print("User already exists.")
        return False
    else:
        users_info[name] = {"password": password, "balance": 1000}
        with open("UsersInfo.json", "w") as file:
            file.write(json.dumps(users_info, indent=4))
        print(f"User {name} added successfully.")
        return True

class Person:
    # Initialize the Person class with name and balance
    def __init__(self, balance=0):
        self.name = None
        self.balance = balance
    
    # Method to handle user login
    def login(self, name, password) -> bool:
        self.name = name

        #Checks if the username exists in the users_info dictionary and if the password matches, then welcomes the user. Otherwise, it prints an error message.
        if self.name in users_info.keys():
            if users_info[self.name]["password"] == password:
                print(f"Welcome, {self.name}!")
                return True
            else:
                print("Invalid password.")
                return False
        else:
            print("User not found.")
            return False
    
    # Method to update the user's balance from the users_info dictionary and optionally export it back to the JSON file
    def update_balance(self, export_balance = False) -> int:
        if export_balance:
            with open(UserInfoFile, "w") as file:
                users_info[self.name]["balance"] = self.balance
                file.write(json.dumps(users_info, indent=4))
            
            print("\nBalance exported and updated successfully")

        else:
            self.balance = users_info[self.name]["balance"]
            with open(UserInfoFile, "w") as file:
                file.write(json.dumps(users_info, indent=4))
            return self.balance

        