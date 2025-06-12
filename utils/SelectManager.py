from utils.TUI import TUI
from queries import *

class SelectManager:
    @staticmethod
    def select_category(db):
        """Displays the available product categories and allows the user to select one."""
        categories = db.fetch_many(GET_CATEGORIES_QUERY)
        if not categories:
            TUI.print_error("No product categories available.\n")
            return None
        return TUI.display_options(categories, "Product Categories", "category")

    @staticmethod
    def select_product(db, category_id):
        """Displays the products in the selected category and allows the user to select one."""
        products = db.fetch_many(GET_PRODUCTS_QUERY, (category_id,))
        if not products:
            TUI.print_error("No products available in this category.\n")
            return None
        return TUI.display_options(products, "Products", "product")

    @staticmethod
    def select_seller(db, product_id):
        """Displays the sellers for the selected product and allows the user to select one."""
        sellers = db.fetch_many(GET_SELLERS_QUERY, (product_id,))
        if not sellers:
            TUI.print_error("No sellers available for this product.\n")
            return None, None
        seller_id = TUI.display_options(
            [(seller[0], f"{seller[1]} - ${seller[2]:.2f}") for seller in sellers],
            "Sellers",
            "seller"
        )
        price = next(seller[2] for seller in sellers if seller[0] == seller_id)
        return seller_id, price