from Users import Person, str_ask, add_user
from SlotMachine import SlotMachine, Results

#Runs the game in a "main" file
def main() -> None:

    #Asks the user for signup or login
    def ask_signup_or_login() -> str:
        while True:
            choice = str_ask("\nDo you want to (1) Sign Up, or (2) Log In? Enter 1 or 2:\n~")
            if choice in ['1', '2']:
                return choice
            else:
                print("\nInvalid choice.")
                continue

    def handle_signup_or_login(choice) -> Person:
        if choice == "1":
            add_user(str_ask("\nEnter a username: "), str_ask("Enter a password: "))
            return handle_signup_or_login("2")
        elif choice == "2": 
                #Login and initialise the player and the balance
                player = Person(str_ask("\nEnter your username: "))
                player.login(str_ask("Enter your password: "))
                player.update_balance()
                return player

    choice = ask_signup_or_login()
    player = handle_signup_or_login(choice)

    
    #Initialise slot machine and game handler
    my_machine = SlotMachine()
    game_handler = Results(my_machine)

    #Plays the game and updates the balance based on win or loss
    game_handler.display_results()
    print(f"\nWinner? : {game_handler.check_win()}")
    player.balance += 100 if game_handler.check_win() else -10
    print(f"\n~~~Current Balance: {player.balance}~~~")
    player.update_balance(export_balance=True)

main()
