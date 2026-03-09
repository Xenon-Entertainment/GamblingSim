import random

class Flip():
    def __init__(self):
        self.choice = "heads"
    def play(self):
        coin_faces = ["heads","tails"]
        chosen = coin_faces[random.randint(0,1)]
        choice = self.choice
        choice = str(input("heads or tails ")).lower()
        if choice.lower() == chosen:
            print("You won")
            return True
        else:
            print("You lost")
            return False