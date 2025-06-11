from tui import TUI
from table import Table
from queries import GET_BASKET_QUERY, GET_BASKET_CONTENTS_QUERY, CREATE_BASKET_QUERY, GET_LAST_INSERT_ID_QUERY


class Basket:
    def __init__(self, shopper_id, db):
        self.items = []
        self.shopper_id = shopper_id
        self.db = db
        self.basket_id = None

    @staticmethod
    def get_basket(db, shopper_id):
        get_basket_query = GET_BASKET_QUERY
        basket = db.fetch_one(get_basket_query, (shopper_id,))
        return basket

    @staticmethod
    def get_basket_contents(db, basket_id):
        get_basket_contents_query = GET_BASKET_CONTENTS_QUERY
        basket_contents = db.fetch_many(get_basket_contents_query, (basket_id,))
        return basket_contents

    @staticmethod
    def display_basket_contents(basket_contents):
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
        db.exe(CREATE_BASKET_QUERY, (shopper_id,))
        return db.fetch_one(GET_LAST_INSERT_ID_QUERY)[0]

    @staticmethod
    def get_most_recent_basket(db, shopper_id):
        query = """
            SELECT basket_id
            FROM shopper_baskets
            WHERE shopper_id = ?
              AND DATE(basket_created_date_time) = DATE('now')
            ORDER BY basket_created_date_time DESC
            LIMIT 1
        """
        result = db.fetch_one(query, (shopper_id,))
        return result[0] if result else None

    def load_items(self):
        if not self.basket_id:
            raise ValueError("Basket ID is not set. Cannot load items.")

        query = """
            SELECT bc.product_id, bc.seller_id, bc.quantity, bc.price
            FROM basket_contents bc
            WHERE bc.basket_id = ?;
        """
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
        basket = cls(shopper_id, db)
        basket.basket_id = cls.get_most_recent_basket(db, shopper_id)
        if basket.basket_id:
            basket.load_items()
        return basket

    def add_item(self, item):
        if item in self.items:
            raise ValueError("Item already exists in the basket.")
        self.items.append(item)

    def remove_item(self, item):
        if item not in self.items:
            raise ValueError("Item not found in the basket.")
        self.items.remove(item)

    def get_items(self):
        return self.items

    def clear(self):
        self.items.clear()

    def __str__(self):
        return f"Basket(shopper_id={self.shopper_id}, items={self.items})"

    def __repr__(self):
        return f"<Basket(shopper_id={self.shopper_id}, basket_id={self.basket_id}, items={len(self.items)})>"