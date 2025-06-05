from db import Database
from tui import TUI

class Controller:
    def __init__(self, db_path):
        self.db = Database(db_path)
        self.shopper = []
        while True:
            self.start()

    def start(self):
        self.main()

    def main(self):
        shoppers = self.db.fetch("SELECT * FROM shoppers;")

        id = input("Please provide a shopper id: ")
        found = list(filter(lambda i: str(i[0]) == id, shoppers))

        if len(found) == 0:
            TUI.print_error("No shopper found.")
            exit()

        self.shopper = found[0]
        TUI.print_success(f"Shopper found! You are now inspecting {self.shopper[2]} {self.shopper[3]}.")

        self.sub()

    def sub(self):
        options = {
            1: "Display your order history",
            2: "Add an item to your basket",
            3: "View your basket",
            4: "Change the quantity of an item in your basket",
            5: "Remove an item from your basket",
            6: "Checkout",
            7: "Exit"
        }

        while True:
            for option in options.items():
                print(f'{option[0]}. {option[1]}')
            selected = int(TUI.validate_input("Please select an option: "))
            if (selected in list(options.keys())):
                print(options(selected))
                break
            else:
                TUI.print_error("Wrong option. ")


if __name__ == "__main__":
    Controller("./db/parana.db")
