
import random as r
from Users import Person
import time

class Bet:
    def __init__(self, length=100, slowest=60, colours=None, horses=6 ):
        self.length = length
        self.slowest = slowest
        self.horses = horses
        self.colours = colours or ["Green", "Red", "Purple", "Blue", "White", "Black", "Magenta", "Perywinkle"] # colour gods
        self.active = None
        self.amount = 0
        self.chosen = None
    def place_bet(self):
        available_colours = self.colours.copy()
        r.shuffle(available_colours)
        print("There are 6 available horses.")
        for i in range(self.horses):
            colour = self.colours[i % len(self.colours)]
            print(f"Horse {i + 1} is colour {colour}")
        while True:
            try:
                horse_choice = int(input(f"\nWhich horse are you betting on? (1-{self.horses}): "))
                if 1 <= horse_choice:
                    self.chosen = horse_choice
                    horse_colour = self.colours[(self.chosen - 1) % len(self.colours)]
                    print(f"Bet placed on Horse {horse_choice}")
                    winner = r.randint(1,6)
                    if winner == self.chosen:
                        print(f"Horse {horse_colour} has won!")
                        return True
                    else:
                        print(f"Horse {horse_colour} lost.")
                        return False
                    break
                else:
                    print("Program Exit")
                    break
            except ValueError:
                print("Enter a valid horse number")
               
                
