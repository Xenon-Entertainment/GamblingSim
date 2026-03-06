import string

from Users import Person, str_ask, add_user
from SlotMachine import SlotMachine, Results
from BlackJack import BlackjackGame, play_blackjack

#Asks the user for signup or login
def ask_signup_or_login() -> str:
    while True:
        choice = str_ask("\nDo you want to,\n(1) Sign Up\nOr,\n(2) Log In?\nEnter 1 or 2:\n~")
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
            player = Person()
            validated = player.login(str_ask("\nEnter your username: "), str_ask("Enter your password: "))
            if validated:
                player.update_balance()
                return player
            else:
                print("\nLogin failed. Please try again.")
                return handle_signup_or_login("2")


def pick_game(game) -> string:
    if game == "1":
        print("\nYou have chosen the Slot Machine!")
        return 1
    elif game =="2":
        print("\nYou have chosen Blackjack!")
        return 2
    else:
        print("\nInvalid choice. Please try again.")
        return pick_game(str_ask("\nWhich game do you want to play? (1) Slot Machine\nOr,\n(2) Blackjack? Enter 1 or 2:\n~"))

def play_game(choice, player) -> None:
    if choice == 1:
        my_machine = SlotMachine()
        game_handler = Results(my_machine)

        #Plays the game and updates the balance based on win or loss
        game_handler.display_results()
        game_handler.output_balance_and_win(player)

    elif choice == 2:
        my_machine = BlackjackGame()
        play_blackjack(player)

#Runs the game in a "main" file
def main() -> None:
    choice = ask_signup_or_login()
    player = handle_signup_or_login(choice)
    #Player is in the person class, Don't worry
    game_choice = pick_game(choice := str_ask("\nWhich game do you want to play? \n(1) Slot Machine or, \n(2) Blackjack?\nEnter 1 or 2:\n~"))
    play_game(game_choice, player)


    

main()
