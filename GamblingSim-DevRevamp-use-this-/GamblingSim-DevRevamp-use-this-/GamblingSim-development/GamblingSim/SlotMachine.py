import random
from Users import Person
import time
from Casinos import get_casino

class SlotMachine:
    def __init__(self, reels=3, symbols=None):
        self.reels = reels
        self.symbols = symbols or ['Cherry', 'Lemon', 'Orange', 'Grape', 'Bell', 'Diamond']
        self.result = []

    def spin(self) -> list:
        self.result = [random.choice(self.symbols) for _ in range(self.reels)]
        return self.result

class Results:
    def __init__(self, machine: SlotMachine, casino=None):
        self.machine = machine
        self.casino = casino or get_casino()
        extra_symbols = self.casino["slot_extra_symbols"]
        self.machine.symbols.extend(
            f"Casino Symbol {number}" for number in range(extra_symbols)
        )

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
    
    def output_balance_and_win(self, player: Person):
        print(f"\nWinner? : {self.check_win()}")
        _change = 1000 if self.check_win() else -10
        print(f"\nBalance: {player.balance} -> {player.balance + _change}")
        player.balance += _change
        player.update_balance(export_balance=True)

    def play(self, player: Person) -> None:
        max_bet = self.casino["bet_limits"]["slot"]
        print(f"\n Player: {player.name} | Balance: ${player.balance} | Table Limit: ${max_bet}")
        while True:
            try:
                bet = int(input(f"Place your bet (1-{max_bet}): $").strip())
                if bet <= 0 or bet > max_bet:
                    print(f"(!) Bet must be between $1 and ${max_bet}.")
                elif bet > player.balance:
                    print(f"(!) Insufficient funds. Your balance is ${player.balance}.")
                else:
                    break
            except ValueError:
                print("(!) Please enter a valid whole number.")

        self.display_results()
        player.balance -= bet
        if self.check_win():
            print("\nWinner! You won $1000.")
            player.balance += bet + 1000
        else:
            print(f"\nNo match. You lost ${bet}.")
        print(f"\nNew balance: ${player.balance}")
        player.update_balance(export_balance=True)
