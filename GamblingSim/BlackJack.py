import random
from Users import Person, str_ask

class BlackjackGame:
    def __init__(self):
        # Creates the deck for the game
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.deck = [f"{r} of {s}" for s in ['Hearts', 'Diamonds', 'Clubs', 'Spades'] for r in ranks]
        random.shuffle(self.deck)
        self.p_hand, self.d_hand = [self.deck.pop(), self.deck.pop()], [self.deck.pop(), self.deck.pop()]
    
    def get_val(self, hand):
        #Loops through the cards and collects the total value
        val, aces = 0, 0
        for card in hand:
            rank = card.split()[0]
            if rank in 'JQK': val += 10
            elif rank == 'A': val += 11; aces += 1
            else: val += int(rank)
        while val > 21 and aces: val -= 10; aces -= 1
        return val

    def show(self, name, hand, final=False):
        # Outputs the results for that specific round
        label = "Dealer" if name == "D" else "Your"
        if name == "D" and not final:
            print(f"Dealer shows: {hand[0]} and [Hidden]")
        else:
            print(f"{label} hand: {hand} | Value: {self.get_val(hand)}")

def play_blackjack(player: Person):
    game = BlackjackGame()
    
    # The players turn
    while game.get_val(game.p_hand) < 21:
        game.show("P", game.p_hand)
        game.show("D", game.d_hand)
        if str_ask("\n(1) Hit or (2) Stand? ") == "1":
            game.p_hand.append(game.deck.pop())
        else: break

    p_val, d_val = game.get_val(game.p_hand), game.get_val(game.d_hand)

    # The dealers turn unless the player did not bust (lose)
    if p_val <= 21:
        while game.get_val(game.d_hand) < 17:
            game.d_hand.append(game.deck.pop())
        d_val = game.get_val(game.d_hand)

    # The utmost final results after all possible things happen essentially
    print("\n--- FINAL RESULTS ---")
    game.show("P", game.p_hand, True)
    game.show("D", game.d_hand, True)

    # The actual scoring logic because yeah
    if p_val > 21: result, change = "Bust! You lose.(Get better)", -20
    elif d_val > 21 or p_val > d_val: result, change = "You win!", 50
    elif p_val < d_val: result, change = "Dealer wins.(You're a loser)", -20
    else: result, change = "It is a draw!", 0

    print(f"{result}\nBalance: {player.balance} -> {player.balance + change}")
    player.balance += change
    player.update_balance(export_balance=True)
    
# Note to subhan this was only so i can test it (you can link it)

""" if __name__ == "__main__":
    p = Person(str_ask("Username: "))
    p.update_balance()
    play_blackjack(p)"""