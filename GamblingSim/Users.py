users_info = {
    "Subhan": {
        "password": "1234",
        "balance": 1000
    }
}

def str_ask(prompt):
    while True:
        value = input(prompt)
        if value.strip() == "":
            print("Input cannot be empty. Please try again.")
        else:
            return value

class Person:
    # Initialize the Person class with name and balance
    def __init__(self, name, balance=0):
        self.name = name
        self.balance = balance
    
    # Method to handle user login
    def login(self, password) -> bool:
        if self.name in users_info and users_info[self.name]["password"] == password:
            print(f"Welcome, {self.name}!")
            return True
        else:
            print("Invalid username or password.")
            return False
    
    # Method to update the user's balance from the users_info dictionary
    def update_balance(self):
        self.balance = users_info[self.name]["balance"]
        return self.balance
        