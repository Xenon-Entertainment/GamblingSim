import random as r
import time
# Change
from Users import Person, str_ask

class Bet:
    def __init__(self, length=100, slowest=60, colours=None, horses=6, balance=100):
        self.length = length
        self.slowest = slowest
        self.horses = horses
        self.colours = colours or ["Green", "Red", "Purple", "Blue", "White", "Black"]
        self.chosen = None
        self.balance = balance  # Tracks medical costs/payouts

def get_valid_input(prompt, valid_options=None, is_int=False, range_limit=None, max_val=None):
    while True:
        try:		
            val = input(prompt).strip().upper()
            if is_int:
                val = int(val)
                # Checks if number is within the specified range if provided
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

def play_horse_race(player):
    race = Bet(horses=6, balance=player.balance)
    injury_scenarios = [
        "suffered a severe tendon strain.",
        "tripped and fractured a fetlock.",
        "pulled a major muscle during the sprint.",
        "showed signs of extreme exhaustion.",
        "collided with the railing."
    ]

    print(f"\n{'='*30}\n      HORSE RACE TRACK      \n{'='*30}")
    print(f" Player: {player.name} | Balance: ${player.balance}")
    
    # Selection logic using the shared helper
    race.chosen = get_valid_input(f"Which horse (1-{race.horses}): ", is_int=True, range_limit=(1, race.horses))
    horse_colour = race.colours[(race.chosen - 1) % len(race.colours)]

    # Animation for the race
    print("\nAnd they're off", end="", flush=True)
    for _ in range(3):
        time.sleep(0.5); print(".", end="", flush=True)
    print("\n")

    # Critical Event (Injury) Logic
    if r.random() < 0.15: # Reduced from 1.0 to 15% for playability, adjust as needed
        injury = r.choice(injury_scenarios)
        print(f"CRITICAL EVENT: Horse {horse_colour} {injury}")
        print("The horse has been retired from the field.")
        print("Medical Bills: -$50")
        player.balance -= 50
    else:
        # Race logic
        winner = r.randint(1, race.horses)
        if winner == race.chosen:
            print(f">> WINNER: Horse {horse_colour} has won! <<")
            payout = 100 # Example payout
            player.balance += payout
            print(f"Winner! You collected ${payout}!")
        else:
            winner_colour = race.colours[(winner - 1) % len(race.colours)]
            print(f"Horse {horse_colour} lost. Winner was Horse {winner} ({winner_colour}).")
            player.balance -= 20 # Example loss
            print(f"Loser! You lost your $20 entry fee.")

    # Update balance logic matching Roulette
    try: 
        player.update_balance(export_balance=True)
    except: 
        pass
    print(f"New Balance: ${player.balance}\n")

# tester
"""
if __name__ == "__main__":
    class MockPlayer:
        def __init__(self):
            self.name, self.balance = "Tester", 1000
        def update_balance(self, export_balance=False): pass 

    test_user = MockPlayer()
    play_horse_race(test_user)
"""