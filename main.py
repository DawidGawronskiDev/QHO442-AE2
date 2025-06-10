from db import Database
from tui import TUI
from shopper import Shopper
from mockup import Mockup

class Controller:
    def __init__(self, db_path):
        self.db = Database(db_path)
        self.shopper = None

        while True:
            self.run()

    def run(self):
        shopper_id = input("Enter Shopper ID: ").strip()
        if not shopper_id.isdigit():
            TUI.print_error("Invalid Shopper ID. Please enter a numeric value.\n")
            return

        shopper_id = int(shopper_id)

        query = f"SELECT * FROM shoppers WHERE shopper_id = {shopper_id}"
        row = self.db.fetch_one(query)
        if row is None:
            TUI.print_error("Shopper not found.\n")
            return

        self.shopper = Shopper(*row)
        self.shopper.init_basket(self.db)
        TUI.print_success(self.shopper.welcome())

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
            TUI.print_list(list(options.values()))
            choice = int(TUI.validate_input("Choose an option: "))

            if choice == 1:
                self.shopper.display_your_order_history(self.db)
                break


if __name__ == "__main__":
    Controller("./db/parana.db")
