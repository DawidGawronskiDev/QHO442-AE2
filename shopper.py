from basket import Basket
from db import Database

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
        self.basket = Basket()
        query = """
            SELECT bc.product_id, bc.seller_id, bc.quantity, bc.price
            FROM basket_contents bc
            INNER JOIN shopper_baskets sb ON bc.basket_id = sb.basket_id
            WHERE sb.shopper_id = ?;
        """
        items = db.fetch_many(query, (self.shopper_id,))
        for item in items:
            self.basket.add_item({
                "product_id": item[0],
                "seller_id": item[1],
                "quantity": item[2],
                "price": item[3]
            })


    def welcome(self):
        return f"Welcome {self.shopper_first_name} {self.shopper_surname}!"