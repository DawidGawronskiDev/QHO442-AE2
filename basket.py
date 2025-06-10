class Basket:
    def __init__(self):
        self.items = []

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

    def load_items(self, db, basket_id):
        query = """
            SELECT bc.product_id, bc.seller_id, bc.quantity, bc.price
            FROM basket_contents bc
            WHERE bc.basket_id = ?;
        """
        items = db.fetch_many(query, (basket_id,))
        for item in items:
            self.add_item({
                "product_id": item[0],
                "seller_id": item[1],
                "quantity": item[2],
                "price": item[3]
            })

    @classmethod
    def initialize(cls, db, shopper_id):
        basket = cls()
        basket_id = cls.get_most_recent_basket(db, shopper_id)
        if basket_id:
            basket.load_items(db, basket_id)
        return basket

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)

    def get_items(self):
        return self.items

    def clear(self):
        self.items.clear()

    def __str__(self):
        return f"Basket(items={self.items})"