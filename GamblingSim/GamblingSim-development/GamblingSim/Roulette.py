import random
import time
#change
from Users import Person, str_ask

class RouletteGame:
    # Creates the roulette wheel first with red numbers and then the rest are black other than 0 which is green
    def __init__(self):
        self.red = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}

    def spin(self):
        res = random.randint(0, 36)
        # Color landed on logic
        color = "GREEN" if res == 0 else ("RED" if res in self.red else "BLACK")
        return res, color

def get_valid_input(prompt, valid_options=None, is_int=False, range_limit=None, max_val=None):
    while True:
        try:
            val = input(prompt).strip().upper()
            if is_int:
                val = int(val)
                #Checks if number is within the specified range if provided
                if range_limit and not (range_limit[0] <= val <= range_limit[1]):
                    print(f"(!) Must be between {range_limit[0]} and {range_limit[1]}.")
                    continue
                # Table limit check
                if max_val and val > max_val:
                    print(f"(!) Over house limit of ${max_val}.")
                    continue
                # No negative bets (or 0)
                if val <= 0:
                    print("(!) Must be greater than 0.")
                    continue
            # Checks for the letters 
            elif valid_options and val not in valid_options:
                print(f"(!) Invalid selection :(. Choose: {', '.join(valid_options)}")
                continue
            return val # Break loop
        except ValueError:
            print("(!) Invalid input. Pretty please enter a number.")

def play_roulette(player):
    game = RouletteGame()
    MAX_BET = 500 # Table limit
    
    print(f"\n{'='*30}\n      ROULETTE TABLE      \n{'='*30}")
    print(f" Player: {player.name} | Balance: ${player.balance} | Table Limit: ${MAX_BET}")
    
    # Bet amount
    bet = get_valid_input("What will your bet be? $", is_int=True, max_val=MAX_BET)
    #Check player balance for bet
    if bet > player.balance:
        print(f"(!) Insufficient funds (Balance: ${player.balance}).")
        return

    # Bet type
    print("\n[N] Number (35:1) | [R] Red | [B] Black | [E] Even | [O] Odd")
    choice = get_valid_input("Select (N/R/B/E/O): ", valid_options=['N', 'R', 'B', 'E', 'O'])
    # Ask for number if they chose to bet on a specific number
    target_num = get_valid_input("Enter number (0-36): ", is_int=True, range_limit=(0, 36)) if choice == 'N' else None

    #Spin the wheel
    print("\nSpinning", end="", flush=True)
    for _ in range(3):
        time.sleep(0.5); print(".", end="", flush=True)
    
    res_n, res_c = game.spin()
    print(f"\n>> BALL LANDED ON: {res_n} ({res_c}) <<")

    # Check win 
    win_conditions = {
        'N': res_n == target_num,
        'R': res_c == "RED",
        'B': res_c == "BLACK",
        'E': res_n % 2 == 0 and res_n != 0,
        'O': res_n % 2 != 0
    }
    
    if win_conditions[choice]:
        payout = 35 if choice == 'N' else 1
        earnings = bet * payout
        total_return = bet + earnings
        print(f"Winner! Your bet won ${earnings}!")

        # Double or nothing option
        if get_valid_input("Double or Nothing? (Y/N): ", valid_options=['Y', 'N']) == 'Y':
            print("\nFlipping", end="", flush=True)
            for _ in range(3):
                time.sleep(0.5); print(".", end="", flush=True)
            if random.choice([True, False]):
                total_return *= 2
                print(f"\nYou win, woohoo! Doubled to ${total_return}!")
                player.balance += (total_return - bet)
            else:
                print("\nOH NO! Lost it all.(You're gonna have to sell your house!)"); player.balance -= bet #Loses basically everything
        else:
            player.balance += earnings
    else:
        player.balance -= bet
        print(f"Loser! You lost ${bet}.")

    try: player.update_balance(export_balance=True)
    except: pass
    print(f"New Balance: ${player.balance}\n")

#Gulp subhan this is my lil test guy because your that guy and the goat so you can link it
"""if __name__ == "__main__":
    class MockPlayer:
        def __init__(self):
            self.name, self.balance = "Tester", 1000
        def update_balance(self, export_balance=False): pass 

    test_user = MockPlayer()
    play_roulette(test_user)"""