import random
import time
from Users import Person, str_ask
from Casinos import get_casino


class Flip:
    def __init__(self):
        self.coin_faces = ["Heads", "Tails"]
        self.choice = None
        self.result = None

    def flip_coin(self, player_win_probability=0.5):
        if self.choice is None:
            return random.choice(self.coin_faces)
        return self.choice if random.random() < player_win_probability else (
            "Tails" if self.choice == "Heads" else "Heads"
        )

    def show_result(self):
        print("\nFlipping coin", end="", flush=True)

        for _ in range(3):
            time.sleep(0.3)
            print(".", end="", flush=True)

        print(f"\n\nThe coin landed on: {self.result}!")

    def play(self, player_win_probability=0.5) -> bool:
        print(f"\n{'=' * 30}")
        print("          COIN FLIP")
        print(f"{'=' * 30}")

        print("\nChoose your side:")
        print("[1] Heads")
        print("[2] Tails")

        while True:
            choice = str_ask("Enter selection:\n~").strip().lower()

            if choice in ["1", "heads"]:
                self.choice = "Heads"
                break
            elif choice in ["2", "tails"]:
                self.choice = "Tails"
                break

            print("(!) Invalid choice. Choose Heads or Tails.")

        print(f"\nYour choice: {self.choice}")

        self.result = self.flip_coin(player_win_probability)
        self.show_result()

        print(f"\n{'>' * 3} FINAL RESULTS {'<' * 3}")

        if self.choice == self.result:
            print("Congratulations! You won!")
            return True

        print("Unlucky! You lost.")
        return False


def play_coin_flip(player: Person, casino=None):
    game = Flip()
    casino = casino or get_casino(getattr(player, "casino_tier", "local"))
    MAX_BET = casino["bet_limits"]["coin_flip"]

    print(f"\n{'=' * 30}")
    print("          COIN FLIP")
    print(f"{'=' * 30}")
    print(f" Player: {player.name} | Balance: ${player.balance}")
    print(f" Maximum bet: ${MAX_BET}")

    # Get a valid bet
    while True:
        try:
            bet = int(str_ask("How much would you like to bet? $").strip())

            if bet <= 0:
                print("(!) Your bet must be greater than $0.")
            elif bet > MAX_BET:
                print(f"(!) The maximum bet is ${MAX_BET}.")
            elif bet > player.balance:
                print(f"(!) Insufficient funds. Your balance is ${player.balance}.")
            else:
                break

        except ValueError:
            print("(!) Please enter a valid whole number.")

    # Play the game
    if game.play(casino["coin_flip_player_win_probability"]):
        print(f"\nYou won ${bet}!")
        player.balance += bet
    else:
        print(f"\nYou lost ${bet}.")
        player.balance -= bet

    # Save the updated balance
    try:
        player.update_balance(export_balance=True)
    except Exception as error:
        print(f"(!) Could not save balance: {error}")

    print(f"New Balance: ${player.balance}\n")


# Tester
"""
if __name__ == "__main__":
    class MockPlayer:
        def __init__(self):
            self.name = "Tester"
            self.balance = 1000

        def update_balance(self, export_balance=False):
            pass

    play_coin_flip(MockPlayer())
"""