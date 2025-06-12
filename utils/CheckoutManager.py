from utils.TUI import TUI
from queries import *

class CheckoutManager:
    @staticmethod
    def process_checkout(db, shopper_id, basket_id, basket_contents):
        """Processes the checkout for the shopper's basket."""
        try:
            db.begin_transaction()

            # Insert into shopper_orders
            db.exe(INSERT_ORDER_QUERY, (shopper_id,))
            order_id = db.fetch_one(GET_LAST_INSERT_ID_QUERY)[0]

            # Insert into ordered_products
            for item in basket_contents:
                product_id, _, _, quantity, price = item
                seller_id = db.fetch_one(
                    GET_SELLER_ID_FROM_BASKET_QUERY,
                    (basket_id, product_id)
                )[0]
                db.exe(INSERT_ORDERED_PRODUCT_QUERY, (order_id, product_id, seller_id, quantity, price))

            # Clear the basket
            db.exe(DELETE_BASKET_CONTENTS_QUERY, (basket_id,))
            db.exe(DELETE_SHOPPER_BASKET_QUERY, (basket_id,))

            db.commit()
            TUI.print_success("Checkout complete, your order has been placed.\n")
        except Exception as e:
            db.rollback()
            TUI.print_error(f"An error occurred during checkout: {e}\n")