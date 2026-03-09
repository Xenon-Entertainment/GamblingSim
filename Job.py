import os
import json

from Users import Person, str_ask

# This class handles the logic for the earning mechanic
class JobSession:
    def __init__(self, player):
        self.player = player
        self.pay_per_press = 10
        self.session_total = 0

    def start_work(self):
        print("\n" + "="*30)
        print(f"--- {self.player.name.upper()}'S JOB ---")
        print(f"Press [ENTER] to earn ${self.pay_per_press}")
        print("Type 'b' to save and go back")
        print("="*30)

        while True:
            # Displays current balance and waits for Enter or 'b'
            action = input(f"Balance: ${self.player.balance} | Shift Total: ${self.session_total} > ").lower().strip()

            if action == 'b':
                # update your balance
                self.player.update_balance(export_balance=True)
                print(f"\nShift over! You earned ${self.session_total} total.")
                break
            else:
                # money
                self.player.balance += self.pay_per_press
                self.session_total += self.pay_per_press
                print(f"  +${self.pay_per_press} Earned!")

# actually runs the freaking code
def start_earning(player):
    job = JobSession(player)
    job.start_work()
