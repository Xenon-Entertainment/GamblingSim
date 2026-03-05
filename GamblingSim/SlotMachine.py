import random
from Users import Person

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
        print(f"Spinning... Result: {self.machine.spin()}")

    def check_win(self) -> bool:
        if not self.machine.result:
            return False
        return all(symbol == self.machine.result[0] for symbol in self.machine.result)

# Usage
my_machine = SlotMachine()
game_handler = Results(my_machine)

game_handler.display_results()
print(f"Winner? {game_handler.check_win()}")
player = Person("Subhan")
player.login("1234")
player.update_balance()
player.balance += 100 if game_handler.check_win() else -10
print(f"Current Balance: {player.balance}")
