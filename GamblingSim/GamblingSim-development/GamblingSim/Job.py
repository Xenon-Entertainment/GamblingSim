import time
import os
import sys

# Standard Windows library for keyboard buffer clearing so itll work on thonny hopefully :) i learnt something new 
try:
    import msvcrt
except ImportError:
    msvcrt = None

class JobSession:
    def __init__(self, player):
        self.player = player
        self.pay_per_press = 10
        self.max_session_earnings = 200
        self.cooldown_period = 60 
        self.session_total = getattr(self.player, 'persistent_session_total', 0)

    def start_work(self):
        current_time = time.time()
        last_session = getattr(self.player, 'last_session_time', 0)
        
        if current_time - last_session < self.cooldown_period:
            remaining = int(self.cooldown_period - (current_time - last_session))
            print(f"Status: Cooldown active. {remaining}s remaining.")
            return

        print(f"\n--- {self.player.name.upper()}'S JOB ---")
        print(f"Rate: ${self.pay_per_press} | Progress: ${self.session_total}/${self.max_session_earnings}")

        while True:
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
                time.sleep(0.25) # Throttle
                self.player.balance += self.pay_per_press
                self.session_total += self.pay_per_press
                print(f"+${self.pay_per_press}")

    def process_exit(self, reached_cap):
        if reached_cap:
            self.player.last_session_time = time.time()
        else:
            self.player.last_session_time = 0

        self.player.update_balance(export_balance=True)
        
        print(f"Session end. Earned: ${self.session_total}. Balance: ${self.player.balance}.")

        #Return to menu anim
        print("Returning", end="")
        for _ in range(3):
            time.sleep(0.4)
            print(".", end="", flush=True)
        
        #buffer fix so that when you spam late input doesn't bleed into main.py
        if msvcrt:
            time.sleep(0.1) 
            while msvcrt.kbhit():
                msvcrt.getch()
        else:
            # same fix but a fall back for Unix-based systems (macOS), (i tried something new here so hopefully it works)
            try:
                import termios
                termios.tcflush(sys.stdin, termios.TCIFLUSH)
            except:
                pass

        #separator for clarity when returning to menu
        print("\n" + "="*30)

def start_earning(player):
    job = JobSession(player)
    job.start_work()

