import random
from Users import Person
import time

class SlotMachine:
    def __init__(self, reels=3, symbols=None):
        self.reels = reels
        self.symbols = symbols or ['Cherry', 'Lemon', 'Orange', 'Grape', 'Bell', 'Diamond']
        self.result = []

    def spin(self) -> list:
        self.result = [random.choice(self.symbols) for _ in range(self.reels)]
        return self.result

class Results:
    def __init__(self, machine: SlotMachine):
        self.machine = machine

    def display_results(self) -> None:
        print("Spinning")
        for _ in range(3):
            time.sleep(0.5)
            print(".", end="", flush=True)
        print(f"\nResult:\n{self.machine.spin()}")

    def check_win(self) -> bool:
        if not self.machine.result:
            return False
        return all(symbol == self.machine.result[0] for symbol in self.machine.result)
