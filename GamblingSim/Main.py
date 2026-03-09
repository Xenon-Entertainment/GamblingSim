import json
import string

#(INTEGRATION) add ur game here
from Users import Person, str_ask, add_user, UserInfoFile
from SlotMachine import SlotMachine, Results
from BlackJack import BlackjackGame, play_blackjack
from Roulette import RouletteGame, play_roulette
from Snap import SnapGame, play_snap

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
            print("\nPlease log in to continue.")
            validated = player.login(str_ask("\nEnter your username: "), str_ask("Enter your password: "))
            if validated:
                player.update_balance()
                return player
            else:
                print("\nLogin failed. Please try again.")
                return handle_signup_or_login("2")


#(INTEGRATION) Add ur game here just follow format and you'll be good
def pick_game(game) -> string:
    if game == "1":
        print("\nYou have chosen the Slot Machine!")
        return 1
    elif game =="2":
        print("\nYou have chosen Blackjack!")
        return 2
    elif game == "3":
        print("\nYou have chosen Roulette!")
        return 3
    elif game == "4":
        print("\nYou have chosen Snap!")
        return 4
    else:
        print("\nInvalid choice. Please try again.")
        #(INTEGRATION) add on option for your game here just follow format and you'll be good
        return pick_game(str_ask("\nWhich game do you want to play? (1) Slot Machine\nOr,\n(2) Blackjack\nOr,\n(3) Roulette\n(4) Snap\nEnter 1, 2, 3, or 4:\n~"))

def play_game(choice, player) -> None:
    if choice == 1:
        my_machine = SlotMachine()
        game_handler = Results(my_machine)

        #Plays the game and updates the balance based on win or loss
        game_handler.display_results()
        game_handler.output_balance_and_win(player)

    #(INTEGRATION) Add ur game here just follow format and you'll be good too
    elif choice == 2:
        my_machine = BlackjackGame()
        play_blackjack(player)

    elif choice == 3:
        my_machine = RouletteGame()
        play_roulette(player)

    elif choice == 4:
        my_machine = SnapGame()
        play_snap(player)


def repeat_game(player) -> None:
    while True:
        choice = str_ask("\nDo you want to play another game? (Y/N),\nOr, view users info(V): ").upper()
        if choice == "Y":
            game_choice = pick_game(str_ask("\nWhich game do you want to play? (1) Slot Machine\nOr,\n(2) Blackjack\nOr,\n(3) Roulette\n(4) Snap\nEnter 1, 2, 3, or 4:\n~"))
            play_game(game_choice, player)
        elif choice == "V":
            users_info_view(printable=True)
        elif choice == "N":
            print("\nThanks for playing! Goodbye!")
            break
        else:
            print("\nInvalid choice. Please enter Y, N, or V.")


def users_info_view(printable = False) -> dict:
    with open(UserInfoFile, "r") as file:
        users_info = json.load(file)
    viewable_users_info = {user: {"balance": info["balance"]} for user, info in users_info.items()}
    viewable_users_info = json.dumps(viewable_users_info, indent=4)
    if not printable:
        pass
    else:
        print(viewable_users_info)
    return viewable_users_info
        
    
    return viewable_users_info

#Runs the game in a "main" file
def main() -> None:
    choice = ask_signup_or_login()
    player = handle_signup_or_login(choice)
    #Player is in the person class, Don't worry

    #View users info, as a player, optional
    while True:
        view_choice = str_ask("\nDo you want to view users info? (Y/N): ").upper()
        if view_choice == "Y":
            users_info_view(printable=True)
            break
        elif view_choice == "N":
            break
        else:
            print("\nInvalid choice. Please enter Y or N.")
            continue

    #(INTEGRATION) Add an option for your game here just follow format and you'll be good
    game_choice = pick_game(choice := str_ask("\nWhich game do you want to play? \n(1) Slot Machine or, \n(2) Blackjack or,\n(3) Roulette or, \n(4) Snap?\nEnter 1, 2, 3, or 4:\n~"))
    play_game(game_choice, player)
    repeat_game(player)


    

main()



