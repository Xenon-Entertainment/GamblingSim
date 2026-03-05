from Users import Person
from SlotMachine import SlotMachine, Results


#Runs the game in a "main" file
def main() -> None:
    my_machine = SlotMachine()
    game_handler = Results(my_machine)

    game_handler.display_results()
    print(f"Winner? {game_handler.check_win()}")
    player = Person("Subhan")
    player.login("1234")
    player.update_balance()
    player.balance += 100 if game_handler.check_win() else -10
    print(f"Current Balance: {player.balance}")

main()
