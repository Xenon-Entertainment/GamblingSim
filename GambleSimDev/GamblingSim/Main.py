import json
from Users import Person, str_ask, add_user, UserInfoFile
from Casinos import CASINOS, CASINO_UNLOCK_COSTS, DEFAULT_CASINO, get_casino

# Games
from SlotMachine import SlotMachine, Results
from BlackJack import BlackjackGame, play_blackjack
from Roulette import RouletteGame, play_roulette
from Snap import SnapGame, play_snap
from Coin_Flip import Flip, play_coin_flip

# Jobs
from Job import start_earning

#(INTEGRATION) add your game in the same format in as the rest here and then add it to the pick_game function below
QUIT_GAME = 300
default = f"\nWhich game do you want to play?\n(1) Slot Machine\n(2) Blackjack\n(3) Roulette\n(4) Snap\n(5) Coin Flip\n(b) Job\n(c) Change casino\n(q) Quit game\nEnter selection:\n~"

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

#(INTEGRATION) I changed it to use mapping instead of if statements for cleaner code and its easier to expand on
def pick_game(game) -> int:
    mapping = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "b": 100, "c": 200, "q": QUIT_GAME}
    if game in mapping:
        if game == "b": print("\nYou have chosen employment!")
        elif game == "c": print("\nYou have chosen to change casinos.")
        elif game == "q": print("\nYou have chosen to quit the game.")
        else: print(f"\nYou have chosen option {game}!")
        return mapping[game]
    print("\nInvalid choice. Please try again.")
    return pick_game(str_ask(default))

#(vs is helping me write the comments teehee)
def confirm_casino_purchase(casino_name, cost) -> bool:
    while True:
        choice = str_ask(f"Are you sure you want to buy {casino_name} for ${cost}? (Y/N): ").upper()
        if choice == "Y":
            return True
        if choice == "N":
            return False
        print("Invalid choice. Please enter Y or N.")

def select_casino(player, allow_keep=False) -> None:
    current = get_casino(getattr(player, "casino_tier", DEFAULT_CASINO))
    print(f"\nCurrent casino: {current['name']}")
    print("Choose a casino:")
    tiers = list(CASINOS.items())
    unlocked_casinos = getattr(player, "unlocked_casinos", [DEFAULT_CASINO])
    for index, (_, casino) in enumerate(tiers, start=1):
        limits = casino["bet_limits"]
        tier = tiers[index - 1][0]
        if tier in unlocked_casinos:
            print(f"({index}) {casino['name']}")
        elif index == len(unlocked_casinos) + 1:
            print(f"({index}) Buy {casino['name']} (${CASINO_UNLOCK_COSTS[tier]})")
        else:
            print(f"({index}) {casino['name']} (unlock previous casino first)")
    if allow_keep:
        print("(0) Keep current casino")

    while True:
        choice = str_ask("Enter selection:\n~")
        if allow_keep and choice == "0":
            return
        if choice.isdigit() and 1 <= int(choice) <= len(tiers):
            tier = tiers[int(choice) - 1][0]
            if tier not in unlocked_casinos:
                if len(unlocked_casinos) + 1 != int(choice):
                    print("Unlock the previous casino first.")
                    continue
                cost = CASINO_UNLOCK_COSTS[tier]
                if player.balance < cost:
                    print(f"You need ${cost} to unlock this casino.")
                    continue
                casino_name = get_casino(tier)["name"]
                if not confirm_casino_purchase(casino_name, cost):
                    print("Casino purchase cancelled.")
                    continue
                player.balance -= cost
                unlocked_casinos.append(tier)
                player.unlocked_casinos = unlocked_casinos
                print(f"Purchased access to {casino_name} for ${cost}.")

            player.casino_tier = tier
            player.update_balance(export_balance=True)
            selected = get_casino(player.casino_tier)
            print(f"Casino set to {selected['name']}.")
            return
        print("Invalid choice. Please choose one of the listed casinos.")

#(INTEGRATION) add game as a choice here
#this block calls the appropriate game function based on the users choice and passes the player object to update balance after the game
def play_game(choice, player) -> None:
    casino = get_casino(getattr(player, "casino_tier", DEFAULT_CASINO))
    if choice == 1:
        my_machine = SlotMachine()
        game_handler = Results(my_machine, casino)
        game_handler.play(player)
    elif choice == 2:
        play_blackjack(player, casino)
    elif choice == 3:
        play_roulette(player, casino)
    elif choice == 4:
        play_snap(player, casino)
    elif choice == 5:
        play_coin_flip(player, casino)
    elif choice == 100:
        start_earning(player, casino)
    elif choice == 200:
        select_casino(player, allow_keep=True)

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
    
    while True:
        #All exiting is routed here
        if game_choice == QUIT_GAME:
            print("\nThanks for playing! Goodbye!")
            break
        play_game(game_choice, player)
        if game_choice in [100, 200]:
            game_choice = pick_game(str_ask(default))
            continue

        while True:
            choice = str_ask("\nDo you want to continue? (Y/N) or View Info (V): ").upper()
            if choice in ["Y", "N", "V"]:
                break
            print("\nInvalid choice.")

        if choice == "Y":
            continue
        elif choice == "N":
            print("\nReturning to the options menu.")
            game_choice = pick_game(str_ask(default))
        elif choice == "V":
            users_info_view(printable=True)

if __name__ == "__main__":
    main()