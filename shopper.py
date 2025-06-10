from db import Database
from basket import Basket
from tui import TUI

class Shopper:
    def __init__(self, shopper_id, shopper_account_ref, shopper_first_name, shopper_surname,
                 shopper_email_address, date_of_birth, gender, date_joined):
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
        self.basket = Basket.initialize(db, self.shopper_id)

    def welcome(self):
        return f"Welcome {self.shopper_first_name} {self.shopper_surname}!"

    def display_your_order_history(self, db: Database):
        query = """
            SELECT
                so.order_id,
                so.order_date,
                p.product_description,
                s.seller_name,
                op.price,
                op.quantity,
                op.ordered_product_status
            FROM shopper_orders so
            JOIN ordered_products op
                ON op.order_id = so.order_id
            JOIN products p
                ON p.product_id = op.product_id
            JOIN sellers s
                ON s.seller_id = op.seller_id
            WHERE shopper_id = ?
            ORDER BY so.order_date DESC;
        """
        rows = db.fetch_many(query, (self.shopper_id,))

        if not len(rows):
            TUI.print_error("No orders placed by this customer")
            return

        # This code needs refactoring
        TUI.print_table(
            (12, 16, 48, 24, 8, 8, 12),
            ("Order ID", "Order Date", "Product Description", "Seller", "Price", "Qty", "Status"),
            rows
        )