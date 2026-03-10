import random
import time
from Users import Person, str_ask

class BlackjackGame:
    def __init__(self):
        # Creates the deck for the game
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.deck = [f"{r} of {s}" for s in ['Hearts', 'Diamonds', 'Clubs', 'Spades'] for r in ranks]
        random.shuffle(self.deck)
        self.p_hand = [self.deck.pop(), self.deck.pop()]
        self.d_hand = [self.deck.pop(), self.deck.pop()]
    
    def get_val(self, hand):
        val, aces = 0, 0
        for card in hand:
            rank = card.split()[0]
            if rank in 'JQK': val += 10
            elif rank == 'A': val += 11; aces += 1
            else: val += int(rank)
        while val > 21 and aces: 
            val -= 10
            aces -= 1
        return val

    def show(self, name, hand, final=False):
        label = "Dealer" if name == "D" else "Your"
        if name == "D" and not final:
            print(f"Dealer shows: {hand[0]} and [Hidden]")
        else:
            print(f"{label} hand: {hand} | Value: {self.get_val(hand)}")

def get_valid_input(prompt, valid_options=None, is_int=False, range_limit=None, max_val=None):
    while True:
        try:
            val = input(prompt).strip().upper()
            if is_int:
                val = int(val)
                if range_limit and not (range_limit[0] <= val <= range_limit[1]):
                    print(f"(!) Must be between {range_limit[0]} and {range_limit[1]}.")
                    continue
                if max_val and val > max_val:
                    print(f"(!) Over house limit of ${max_val}.")
                    continue
                if val <= 0:
                    print("(!) Must be greater than 0.")
                    continue
            elif valid_options and val not in valid_options:
                print(f"(!) Invalid selection :(. Choose: {', '.join(valid_options)}")
                continue
            return val
        except ValueError:
            print("(!) Invalid input. Pretty please enter a number.")

def play_blackjack(player: Person):
    game = BlackjackGame()
    MAX_BET = 500 # Table limit
    
    print(f"\n{'='*30}\n      BLACKJACK TABLE      \n{'='*30}")
    print(f" Player: {player.name} | Balance: ${player.balance} | Table Limit: ${MAX_BET}")
    
    # Bet amount
    bet = get_valid_input("What will your bet be? $", is_int=True, max_val=MAX_BET)
    
    # Check player balance for bet
    if bet > player.balance:
        print(f"(!) Insufficient funds (Balance: ${player.balance}).")
        return

    # Natural Blackjack check (To make it harder to lose "all the time")
    p_val = game.get_val(game.p_hand)
    if p_val == 21:
        print("\n>> NATURAL BLACKJACK! <<")
        game.show("P", game.p_hand, True)
        earnings = int(bet * 1.5)
        print(f"Winner! Your blackjack won ${earnings}!")
        player.balance += earnings
    else:
        # Player's turn
        while p_val < 21:
            print("\n--- CURRENT HANDS ---")
            game.show("P", game.p_hand)
            game.show("D", game.d_hand)
            
            choice = get_valid_input("\n[1] Hit | [2] Stand: ", valid_options=['1', '2'])
            if choice == "1":
                print("\nDealing", end="", flush=True)
                for _ in range(3):
                    time.sleep(0.3); print(".", end="", flush=True)
                game.p_hand.append(game.deck.pop())
                p_val = game.get_val(game.p_hand)
                if p_val > 21:
                    print(f"\n>> BUSTED! ({p_val}) <<")
            else:
                break

        # Dealer's turn
        d_val = game.get_val(game.d_hand)
        if p_val <= 21:
            print("\nDealer's turn", end="", flush=True)
            while d_val < 17:
                for _ in range(3):
                    time.sleep(0.3); print(".", end="", flush=True)
                game.d_hand.append(game.deck.pop())
                d_val = game.get_val(game.d_hand)

        # Final Scoring
        print(f"\n\n{'>'*3} FINAL RESULTS {'<'*3}")
        game.show("P", game.p_hand, True)
        game.show("D", game.d_hand, True)

        if p_val > 21:
            print(f"Loser! You busted and lost ${bet}, Idiot.")
            player.balance -= bet
        elif d_val > 21:
            print(f"Very special cool guy! Dealer busted. You won ${bet}!, dealer was an idiot this time.")
            player.balance += bet
        elif p_val > d_val:
            print(f"Winner! Your score is higher. You won ${bet}!")
            player.balance += bet
        elif p_val < d_val:
            print(f"Loser! Dealer score is higher. You lost ${bet}.")
            player.balance -= bet
        else:
            print("It's a draw! Your bet was returned.")

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
    play_blackjack(test_user)
"""
