import random

class Flip():
    def __init__(self):
        self.choice = "heads"
        
    def play(self, player):
        coin_faces = ["H","T"]
        chosen = coin_faces[random.randint(0,1)]
        choice = self.choice
        choice = str(input("\nHeads or Tails (H/T): ")).lower()
        if choice.lower() == chosen:
            print("\nYou won")
            print(f"{player.balance}->{player.balance+10}")
            player.balance += 100
            player.update_balance(export_balance=True)            
            return True
        else:
            print("You lost")
            print(f"\nPlayer balance:\n{player.balance} -> {player.balance-10}")
            player.balance += -10
            player.update_balance(export_balance=True)
            return False
    
        