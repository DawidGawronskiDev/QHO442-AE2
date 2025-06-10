from shopper import Shopper
from db import Database
from tui import TUI

class Mockup:
    def __init__(self, db: Database, shopper_id):
        self.db = db
        self.shopper_id = shopper_id
        self.shopper = None

        self.start()

    def start(self):
        query = """
            SELECT * FROM shoppers WHERE shopper_id = ?;
        """
        result = self.db.fetch_one(query, (self.shopper_id,))
        self.shopper = Shopper(*result)

        self.display_your_order_history()


    def display_your_order_history(self):
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
            ORDER BY so.order_date ASC;
        """
        rows = self.db.fetch_many(query, (self.shopper.shopper_id,))

        if not len(rows):
            TUI.print_error("No orders placed by this customer")

        lens = (12, 16, 48, 24, 8, 8, 12)
        header = ("Order ID", "Order Date", "Product Description", "Seller", "Price", "Qty", "Status")
        for i, val in enumerate(header):
            print(str(val).strip()[:lens[i]].ljust(lens[i], " "), end="")
        print("\n")
        for row in rows:
            for i, val in enumerate(row):
                print(str(val).strip()[:lens[i]].ljust(lens[i], " "), end="")
            print("\n")