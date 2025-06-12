from utils.Database import Database
from utils.Basket import Basket
from utils.TUI import TUI
from utils.Table import Table
from queries import GET_ORDER_HISTORY_QUERY

class Shopper:
    """A class representing a shopper in the system."""
    def __init__(self, shopper_id, shopper_account_ref, shopper_first_name, shopper_surname,
                 shopper_email_address, date_of_birth, gender, date_joined):
        """
        Initializes a new Shopper instance.
        """
        self.shopper_id = shopper_id
        self.shopper_account_ref = shopper_account_ref
        self.shopper_first_name = shopper_first_name
        self.shopper_surname = shopper_surname
        self.shopper_email_address = shopper_email_address
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.date_joined = date_joined
        self.basket = None

    def init_basket(self, db: Database):
        """ Initializes the shopper's basket. """
        self.basket = Basket.initialize(db, self.shopper_id)

    def welcome(self):
        """ Returns a welcome message for the shopper. """
        return f"Welcome {self.shopper_first_name} {self.shopper_surname}!"

    def display_your_order_history(self, db: Database):
        """ Displays the order history for the shopper. """
        rows = db.fetch_many(GET_ORDER_HISTORY_QUERY, (self.shopper_id,))

        if not len(rows):
            TUI.print_error("No orders placed by this customer")
            return

        # This code needs refactoring
        Table(
            (12, 16, 96, 24, 8, 8, 12),
            ("Order ID", "Order Date", "Product Description", "Seller", "Price", "Qty", "Status"),
            rows
        ).print_table()