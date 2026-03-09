import json
import os

basedir = os.path.dirname(os.path.abspath(__file__))
UserInfoFile = os.path.join(basedir, "UsersInfo.json")

users_info = {}
try:
    with open(UserInfoFile, "r") as file:
        users_info = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    users_info = {}

def str_ask(prompt):
    while True:
        value = input(prompt).strip()
        if value == "":
            print("Input cannot be empty.")
            continue
        return value

#Still the same as subhans method kinda, but it allows more things
def add_user(name, password) -> bool:
    if name in users_info:
        print("User already exists.")
        return False
    
    users_info[name] = {
        "password": password, 
        "balance": 1000,
        "persistent_session_total": 0,
        "last_session_time": 0
    }
    with open(UserInfoFile, "w") as file:
        json.dump(users_info, file, indent=4)
    print(f"User {name} added.")
    return True

class Person:
    # still initializes the person class with name and balance but with added job data
    def __init__(self, balance=0):
        self.name = None
        self.balance = balance
        self.persistent_session_total = 0
        self.last_session_time = 0
    
    #Handles user login but with a lot safer handling and it also loads the job data for the user
    #Still sees if user is authenticated and welcomes and if not prints error message
    def login(self, name, password) -> bool:
        if name in users_info and users_info[name]["password"] == password:
            self.name = name
            data = users_info[name]
            self.balance = data.get("balance", 0)
            self.persistent_session_total = data.get("persistent_session_total", 0)
            self.last_session_time = data.get("last_session_time", 0)
            print(f"Welcome, {self.name}!")
            return True
        print("User not found or incorrect password.")
        return False
    
    # Method to update the user's balance and job data in the JSON file(users_info), or load it if export_balance is False
    def update_balance(self, export_balance=False) -> int:
        if not self.name:
            return self.balance

        if export_balance:
            users_info[self.name].update({
                "balance": self.balance,
                "persistent_session_total": self.persistent_session_total,
                "last_session_time": self.last_session_time
            })
            with open(UserInfoFile, "w") as file:
                json.dump(users_info, file, indent=4)
        else:
            data = users_info[self.name]
            self.balance = data.get("balance", 0)
            self.persistent_session_total = data.get("persistent_session_total", 0)
            self.last_session_time = data.get("last_session_time", 0)
            
        return self.balance

        

