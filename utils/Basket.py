from utils.TUI import TUI
from utils.Table import Table
from queries import *


class Basket:
    """A class representing a shopping basket for a shopper."""
    def __init__(self, shopper_id, db):
        """
        Initializes a new Basket instance.
        """
        self.items = []
        self.shopper_id = shopper_id
        self.db = db
        self.basket_id = None

    @staticmethod
    def get_basket(db, shopper_id):
        """ Retrieves the basket for a given shopper ID."""
        get_basket_query = GET_BASKET_QUERY
        basket = db.fetch_one(get_basket_query, (shopper_id,))
        return basket

    @staticmethod
    def get_basket_contents(db, basket_id):
        """ Retrieves the contents of a basket by its ID."""
        get_basket_contents_query = GET_BASKET_CONTENTS_QUERY
        basket_contents = db.fetch_many(get_basket_contents_query, (basket_id,))
        return basket_contents

    @staticmethod
    def display_basket_contents(basket_contents):
        """ Displays the contents of the basket in a formatted table."""
        rows = []
        total_cost = 0
        for idx, item in enumerate(basket_contents, start=1):
            product_id, product_description, seller_name, quantity, price = item
            item_total = quantity * price
            total_cost += item_total
            rows.append((
                idx,
                product_description,
                seller_name,
                quantity,
                f"£{price:.2f}",
                f"£{item_total:.2f}"
            ))

        TUI.print_header("Basket Contents")
        Table((12, 64, 24, 8, 12, 12),
              ("Item No.", "Description", "Seller", "Qty", "Price", "Total"),
              rows).print_table()

        print(f"\nBasket Total: £{total_cost:.2f}\n")

    @staticmethod
    def create_basket(db, shopper_id):
        """ Creates a new basket for the given shopper ID."""
        db.exe(CREATE_BASKET_QUERY, (shopper_id,))
        return db.fetch_one(GET_LAST_INSERT_ID_QUERY)[0]

    @staticmethod
    def get_most_recent_basket(db, shopper_id):
        """ Retrieves the most recent basket ID for a shopper."""
        query = GET_MOST_RECENT_BASKET_QUERY
        result = db.fetch_one(query, (shopper_id,))
        return result[0] if result else None

    def load_items(self):
        """ Loads items from the database into the basket."""
        if not self.basket_id:
            raise ValueError("Basket ID is not set. Cannot load items.")

        query = GET_BASKET_CONTENTS_FOR_CHECKOUT_QUERY
        items = self.db.fetch_many(query, (self.basket_id,))
        self.items = [
            {
                "product_id": item[0],
                "seller_id": item[1],
                "quantity": item[2],
                "price": item[3]
            }
            for item in items
        ]

    @classmethod
    def initialize(cls, db, shopper_id):
        """ Initializes a basket for a shopper, loading existing items if available."""
        basket = cls(shopper_id, db)
        basket.basket_id = cls.get_most_recent_basket(db, shopper_id)
        if basket.basket_id:
            basket.load_items()
        return basket

    def __str__(self):
        """ Returns a string representation of the basket."""
        return f"Basket(shopper_id={self.shopper_id}, items={self.items})"