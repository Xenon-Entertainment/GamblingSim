import random
import time
#change (i use change so i dont forget how to integrate)
from Users import Person, str_ask

class SnapGame:
    def __init__(self):
        # Creates the deck but without the classes because it is useless to have them for this game and im lazy
        self.deck = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'] * 4
        random.shuffle(self.deck)

    def deal(self):
        # Splits deck between player and dealer so u can do your thing
        return self.deck[:26], self.deck[26:]

#idk if u can tell but i basically just copy and pasted my code from roulette because again im lazy and it works so why not
def get_valid_input(prompt, valid_options=None, is_int=False, max_val=None):
    while True:
        try:
            val = input(prompt).strip().upper()
            if is_int:
                val = int(val)
                if max_val and val > max_val:
                    print(f"(!) Over house limit of ${max_val}.")
                    continue
                if val <= 0:
                    print("(!) Must be greater than 0.")
                    continue
            elif valid_options and val not in valid_options:
                print(f"(!) Invalid selection. Choose: {', '.join(valid_options)}")
                continue
            return val
        except ValueError:
            print("(!) Invalid input. Please enter a number.")

def play_snap(player):
    game = SnapGame()
    MAX_BET = 200 # I think we get that this is the table limit from roulette
    player_hand, dealer_hand = game.deal()
    print(f"\n{'='*30}\n       CASINO SNAP     \n{'='*30}")
    print(f" Player: {player.name} | Balance: ${player.balance} | Table Limit: ${MAX_BET}")
    
    bet = get_valid_input("Place your bet for the round: $", is_int=True, max_val=MAX_BET)
    if bet > player.balance:
        print(f"(!) Insufficient funds.")
        return

    print("\nRULES: Cards will be flipped. If they match, type 'S' and enter as fast as possible!")
    print("Press ENTER to start the round...")
    input()

    pot = bet * 2
    last_card = None
    
    while len(player_hand) > 0 and len(dealer_hand) > 0:
        input("--- Press ENTER to flip the next card ---")
        
        # the flips to possibly create a pair
        card1 = dealer_hand.pop(0)
        print(f"DEALER flips: [{card1}]")
        time.sleep(0.5)
        
        card2 = player_hand.pop(0)
        print(f"YOU flip: [{card2}]")
        time.sleep(0.5)

        # match check
        if card1 == card2:
            start_time = time.time()
            reaction = input("!!! MATCH !!! TYPE 'S' to SNAP: ").strip().upper()
            end_time = time.time()
            reaction_time = end_time - start_time

            # Dealer reaction simulation
            dealer_speed = random.uniform(0.8, 1.8)

            if reaction == "S" and reaction_time < dealer_speed:
                print(f"\nSpeedy Boy! You snapped in {reaction_time:.2f}s!")
                print(f"Dealer was a bit behind ({dealer_speed:.2f}s).")
                print(f"You win all the money and can buy your house back: ${pot}")
                player.balance += bet
                break
            else:
                print(f"\nSlowpoke! Dealer snapped in {dealer_speed:.2f}s.")
                print(f"Your time: {reaction_time:.2f}s.")
                player.balance -= bet
                break
        else:
            print("No match. Moving to next cards...")
            # Continue until a match or cards run out
            if len(player_hand) == 0:
                print("\nOut of cards! It's a Draw. Bet returned.")
                break

    try: 
        player.update_balance(export_balance=True)
    except: 
        pass
    print(f"New Balance: ${player.balance}\n")

# Tester guy
"""if __name__ == "__main__":
    class MockPlayer:
        def __init__(self):
            self.name, self.balance = "Tester", 1000
        def update_balance(self, export_balance=False): pass 

    test_user = MockPlayer()
    #change this to be specific to your module if u want to use it subhan or seb its lowkey goated to test so you know you wont break main
    play_snap(test_user)"""