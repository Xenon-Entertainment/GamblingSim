import json
import string
from Users import Person, str_ask, add_user, UserInfoFile

# Games
from SlotMachine import SlotMachine, Results
from BlackJack import BlackjackGame, play_blackjack
from Roulette import RouletteGame, play_roulette
from Snap import SnapGame, play_snap
from horse_bets import play_horse_race
from coin_Flip import Flip

# Jobs
from Job import start_earning

#(INTEGRATION) add your game in the same format in as the rest here and then add it to the pick_game function below
default = f"\nWhich game do you want to play?\n(1) Slot Machine\n(2) Blackjack\n(3) Roulette\n(4) Snap\n(5) Horse Bet\n(6) Coin Flip\n(b) Job\nEnter selection:\n~"

def ask_signup_or_login() -> str:
    while True:
        choice = str_ask("\n(1) Sign Up\n(2) Log In\nEnter 1 or 2:\n~")
        if choice in ['1', '2']: return choice
        print("\nInvalid choice.")

def handle_signup_or_login(choice) -> Person:
    if choice == "1":
        # new sign up flow with an escape route to login if they accidentally chose sign up or vice versa
        add_user(str_ask("\nEnter a username: "), str_ask("Enter a password: "))
        return handle_signup_or_login("2")
    
    elif choice == "2": 
        player = Person()
        print("\nPlease log in to continue.")
        while True:
            username = str_ask("\nEnter your username: ")
            password = str_ask("Enter your password: ")
            
            if player.login(username, password):
                player.update_balance()
                return player
            else:
                # the escape route for users who choose login but dont have an account or remember their credentials
                print("\nLogin failed.")
                retry = str_ask("Would you like to (1) Try again or (2) Sign up instead?\n~")
                
                if retry == "2":
                    return handle_signup_or_login("1")
                # if they pick 1 it just loops back to the login prompts
                print("\nRestarting login...")

#I changed it to use mapping instead of if statements for cleaner code and its easier to expand on
def pick_game(game) -> int:
    mapping = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "b": 100}
    if game in mapping:
        if game == "b": print("\nYou have chosen employment!")
        else: print(f"\nYou have chosen option {game}!")
        return mapping[game]
    print("\nInvalid choice. Please try again.")
    return pick_game(str_ask(default))


#(INTEGRATION) add game as a choice here
#this block calls the appropriate game function based on the users choice and passes the player object to update balance after the game
#(vs is helping me right the comments teehee)
def play_game(choice, player) -> None:
    if choice == 1:
        my_machine = SlotMachine()
        game_handler = Results(my_machine)
        game_handler.display_results()
        game_handler.output_balance_and_win(player)
    elif choice == 2:
        play_blackjack(player)
    elif choice == 3:
        play_roulette(player)
    elif choice == 4:
        play_snap(player)
    elif choice == 5:
        play_horse_race(player)
    elif choice == 6:
        sus = Flip()
        if sus.play(): player.balance += 100
        else: player.balance -= 10
    elif choice == 100:
        start_earning(player)

#views user info
def users_info_view(printable = False) -> str:
    with open(UserInfoFile, "r") as file:
        users_info = json.load(file)
    viewable_users_info = {user: {"balance": info["balance"]} for user, info in users_info.items()}
    formatted_info = json.dumps(viewable_users_info, indent=4)
    if printable: print(formatted_info)
    return formatted_info

#runs the rawtid code
def main() -> None:
    choice = ask_signup_or_login()
    player = handle_signup_or_login(choice)
    
    while True:
        view_choice = str_ask("\nDo you want to view users info? (Y/N): ").upper()
        if view_choice == "Y":
            users_info_view(printable=True)
            break
        elif view_choice == "N": break
        print("\nInvalid choice.")

    game_choice = pick_game(str_ask(default))
    play_game(game_choice, player)
    
    while True:
        choice = str_ask("\nDo you want to play another game? (Y/N) or View Info (V): ").upper()
        if choice == "Y":
            play_game(pick_game(str_ask(default)), player)
        elif choice == "V":
            users_info_view(printable=True)
        elif choice == "N":
            print("\nThanks for playing! Goodbye!")
            break
        else:
            print("\nInvalid choice.")

if __name__ == "__main__":
    main()












