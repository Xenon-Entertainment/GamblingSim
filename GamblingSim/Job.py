import os
import json
import time

from Users import Person, str_ask

class JobSession:
    def __init__(self, player):
        self.player = player
        self.pay_per_press = 10
        self.max_session_earnings = 200
        self.cooldown_period = 60 # cooldown does reset when the code is run again so can be glitched by restarting the program
        # Initialize session total from player data
        self.session_total = getattr(self.player, 'persistent_session_total', 0)

    def start_work(self):
        current_time = time.time()
        last_session = getattr(self.player, 'last_session_time', 0)
        
        # verifies the cooldown period and prevents starting a new session if still active
        if current_time - last_session < self.cooldown_period:
            remaining = int(self.cooldown_period - (current_time - last_session))
            print(f"Status: Cooldown active. {remaining}s remaining.")
            return

        print(f"\n--- {self.player.name.upper()}'S JOB ---")
        print(f"Rate: ${self.pay_per_press} | Progress: ${self.session_total}/${self.max_session_earnings}")

        while True:
            # checks if the session earnings have reached the cap and initiates cooldown if so
            if self.session_total >= self.max_session_earnings:
                print("Status: Session cap reached. Cooldown Activated.")
                self.player.persistent_session_total = 0 
                self.process_exit(reached_cap=True)
                break

            action = input(f"Bal: ${self.player.balance} | Session: ${self.session_total} > ").lower().strip()

            if action == 'b':
                self.player.persistent_session_total = self.session_total
                self.process_exit(reached_cap=False)
                break
            else:
                self.player.balance += self.pay_per_press
                self.session_total += self.pay_per_press
                print(f"+${self.pay_per_press}")

    def process_exit(self, reached_cap):
        """Synchronization of player data and exit animation."""
        if reached_cap:
            self.player.last_session_time = time.time()
        else:
            self.player.last_session_time = 0

        self.player.update_balance(export_balance=True)
        
        print(f"Session end. Earned: ${self.session_total}. Balance: ${self.player.balance}.")
        print("Returning", end="")
        for _ in range(3):
            time.sleep(0.5)
            print(".", end="", flush=True)
        print()

def start_earning(player):
    job = JobSession(player)
    job.start_work()
