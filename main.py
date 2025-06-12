from utils.Database import Database
from utils.Validator import Validator
from utils.Shopper import Shopper
from utils.TUI import TUI
from utils.Basket import Basket
from utils.SelectManager import SelectManager
from utils.CheckoutManager import CheckoutManager
from utils.MenuManager import MenuManager
from queries import *


class Controller:
    """Controller class to manage the interaction between the user and the database."""
    def __init__(self, db_path):
        """Initializes the Controller with a database connection."""
        self.db = Database(db_path)
        self.shopper = None
        self.basket = None

        while True:
            self.run()

    def run(self):
        """Main method to run the controller."""
        shopper_id = Validator.validate_numeric_input(
            "Enter Shopper ID: ",
            "Invalid Shopper ID. Please enter a numeric value.",
            min_value=1
        )

        row = self.db.fetch_one(GET_SHOPPERS_QUERY, (shopper_id,))
        if row is None:
            TUI.print_error("Shopper not found.\n")
            exit()

        self.shopper = Shopper(*row)
        self.shopper.init_basket(self.db)
        self.basket = Basket(self.shopper.shopper_id, self.db)
        TUI.print_success(self.shopper.welcome())

        MenuManager(self).display_menu()

    def sub_1(self):
        """Displays the order history for the shopper."""
        self.shopper.display_your_order_history(self.db)

    def sub_2(self):
        """Adds an item to the shopper's basket."""
        category_id = SelectManager.select_category(self.db)
        if not category_id:
            return

        product_id = SelectManager.select_product(self.db, category_id)
        if not product_id:
            return

        seller_id, price = SelectManager.select_seller(self.db, product_id)
        if not seller_id:
            return

        quantity = Basket.get_quantity()
        if not quantity:
            return

        basket_id = Basket.get_or_create_basket(self.db, self.shopper.shopper_id)[0]

        try:
            Basket.add_item_to_basket(self.db, basket_id, product_id, seller_id, quantity, price)
            TUI.print_success("Item added to your basket.\n")
        except Exception as e:
            TUI.print_error(f"An error occurred while adding the item to your basket: {e}\n")
            return

    def sub_3(self):
        """Displays the contents of the shopper's basket."""
        if Basket.is_basket_empty(self.db, self.shopper.shopper_id):
            return
        basket_contents = Basket.get_basket_contents(self.db, Basket.get_basket(self.db, self.shopper.shopper_id)[0])
        Basket.display_basket_contents(basket_contents)

    def sub_4(self):
        """Displays the contents of the shopper's basket and allows them to change item quantities."""
        if Basket.is_basket_empty(self.db, self.shopper.shopper_id):
            return
        basket_contents = Basket.get_basket_contents(self.db, Basket.get_basket(self.db, self.shopper.shopper_id)[0])
        Basket.display_basket_contents(basket_contents)

        Basket.display_basket_contents(basket_contents)

        item_no = Basket.select_basket_item(basket_contents)
        if item_no is None:
            return

        selected_item = basket_contents[item_no - 1]
        product_id = selected_item[0]

        new_quantity = Basket.get_new_quantity()
        if new_quantity is None:
            return

        Basket.update_item_quantity(
            self.db,
            Basket.get_basket(self.db, self.shopper.shopper_id)[0],
            product_id,
            new_quantity
        )
        TUI.print_success("Quantity updated successfully.\n")

        self.sub_3()

    def sub_5(self):
        """Displays the contents of the shopper's basket and allows them to remove items."""
        if Basket.is_basket_empty(self.db, self.shopper.shopper_id):
            return
        basket_contents = Basket.get_basket_contents(self.db, Basket.get_basket(self.db, self.shopper.shopper_id)[0])
        Basket.display_basket_contents(basket_contents)

        item_no = Basket.select_basket_item(basket_contents)
        if item_no is None:
            return

        selected_item = basket_contents[item_no - 1]
        product_id = selected_item[0]

        confirm_removal = Validator.validate_confirmation(
            "Are you sure you want to remove this item from your basket? (Y/N): ",
            "Invalid input. Please enter Y or N."
        )
        if not confirm_removal:
            TUI.print_success("Item removal canceled.\n")
            return

        Basket.remove_item_from_basket(
            self.db,
            Basket.get_basket(self.db, self.shopper.shopper_id)[0],
            product_id
        )
        TUI.print_success("Item removed successfully.\n")

        basket_contents = Basket.get_basket_contents(self.db, Basket.get_basket(self.db, self.shopper.shopper_id)[0])
        if not basket_contents:
            TUI.print_error("Your basket is empty.\n")
            return

        Basket.display_basket_contents(basket_contents)

    def sub_6(self):
        """Processes the checkout for the shopper's basket."""
        if Basket.is_basket_empty(self.db, self.shopper.shopper_id):
            return
        basket_contents = Basket.get_basket_contents(self.db, Basket.get_basket(self.db, self.shopper.shopper_id)[0])
        Basket.display_basket_contents(basket_contents)

        confirm_checkout = Validator.validate_confirmation(
            "Are you sure you want to checkout? (Y/N): ",
            "Invalid input. Please enter Y or N."
        )
        if not confirm_checkout:
            TUI.print_success("Checkout canceled.\n")
            return

        CheckoutManager.process_checkout(
            self.db,
            self.shopper.shopper_id,
            Basket.get_basket(self.db, self.shopper.shopper_id)[0],
            basket_contents
        )


if __name__ == "__main__":
    Controller("db/parana.db")
