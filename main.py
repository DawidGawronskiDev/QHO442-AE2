from db import Database
from tui import TUI
from shopper import Shopper
from basket import Basket
from table import Table
from queries import *

class Controller:
    def __init__(self, db_path):
        self.db = Database(db_path)
        self.shopper = None
        self.basket = None

        while True:
            self.run()

    def run(self):
        shopper_id = input("Enter Shopper ID: ").strip()
        if not shopper_id.isdigit():
            TUI.print_error("Invalid Shopper ID. Please enter a numeric value.\n")
            return

        shopper_id = int(shopper_id)

        row = self.db.fetch_one(GET_SHOPPERS_QUERY, (shopper_id,))
        if row is None:
            TUI.print_error("Shopper not found.\n")
            return

        self.shopper = Shopper(*row)
        self.shopper.init_basket(self.db)
        self.basket = Basket(self.shopper.shopper_id, self.db)
        TUI.print_success(self.shopper.welcome())

        self.sub()

    def sub(self):
        options = {
            1: "Display your order history",
            2: "Add an item to your basket",
            3: "View your basket",
            4: "Change the quantity of an item in your basket",
            5: "Remove an item from your basket",
            6: "Checkout",
            7: "Exit"
        }

        actions = {
            1: self.sub_1,
            2: self.sub_2,
            3: self.sub_3,
            4: self.sub_4,
            5: self.sub_5,
            6: self.sub_6,
            7: exit
        }

        while True:
            for option in options.items():
                print(f"{option[0]}: {option[1]}")
            choice = int(input("Choose an option: ").strip())

            if choice in options.keys():
                actions[choice]()

    def sub_1(self):
        self.shopper.display_your_order_history(self.db)

    def sub_2(self):
        category_id = self.select_category()
        if not category_id:
            return

        product_id = self.select_product(category_id)
        if not product_id:
            return

        seller_id, price = self.select_seller(product_id)
        if not seller_id:
            return

        quantity = self.get_quantity()
        if not quantity:
            return

        basket_id = self.get_or_create_basket()
        self.add_item_to_basket(basket_id, product_id, seller_id, quantity, price)

        TUI.print_success("Item added to your basket.\n")

    def sub_3(self):
        basket = self.get_basket()
        if not basket:
            TUI.print_error("Your basket is empty.\n")
            return

        basket_contents = self.get_basket_contents(basket[0])
        if not basket_contents:
            TUI.print_error("Your basket is empty.\n")
            return

        self.display_basket_contents(basket_contents)

    def sub_4(self):
        basket = self.get_basket()
        if not basket:
            TUI.print_error("Your basket is empty.\n")
            return

        basket_contents = self.get_basket_contents(basket[0])
        if not basket_contents:
            TUI.print_error("Your basket is empty.\n")
            return

        self.display_basket_contents(basket_contents)

        item_no = self.select_basket_item(basket_contents)
        if item_no is None:
            return

        selected_item = basket_contents[item_no - 1]
        product_id = selected_item[0]

        new_quantity = self.get_new_quantity()
        if new_quantity is None:
            return

        self.update_item_quantity(basket[0], product_id, new_quantity)
        TUI.print_success("Quantity updated successfully.\n")

        self.sub_3()

    def sub_5(self):
        basket = self.get_basket()
        if not basket:
            TUI.print_error("Your basket is empty.\n")
            return

        basket_contents = self.get_basket_contents(basket[0])
        if not basket_contents:
            TUI.print_error("Your basket is empty.\n")
            return

        self.display_basket_contents(basket_contents)

        item_no = self.select_basket_item(basket_contents)
        if item_no is None:
            return

        selected_item = basket_contents[item_no - 1]
        product_id = selected_item[0]

        if not self.confirm_removal():
            TUI.print_success("Item removal canceled.\n")
            return

        self.remove_item_from_basket(basket[0], product_id)
        TUI.print_success("Item removed successfully.\n")

        basket_contents = self.get_basket_contents(basket[0])
        if not basket_contents:
            TUI.print_error("Your basket is empty.\n")
            return

        self.display_basket_contents(basket_contents)

    def sub_6(self):
        basket = self.get_basket()
        if not basket:
            TUI.print_error("Your basket is empty.\n")
            return

        basket_contents = self.get_basket_contents(basket[0])
        if not basket_contents:
            TUI.print_error("Your basket is empty.\n")
            return

        self.display_basket_contents(basket_contents)

        if not self.confirm_checkout():
            TUI.print_success("Checkout canceled.\n")
            return

        self.process_checkout(basket[0], basket_contents)

    def select_category(self):
        categories = self.db.fetch_many(GET_CATEGORIES_QUERY)
        if not categories:
            TUI.print_error("No product categories available.\n")
            return None
        return TUI.display_options(categories, "Product Categories", "category")

    def select_product(self, category_id):
        products = self.db.fetch_many(GET_PRODUCTS_QUERY, (category_id,))
        if not products:
            TUI.print_error("No products available in this category.\n")
            return None
        return TUI.display_options(products, "Products", "product")

    def select_seller(self, product_id):
        sellers = self.db.fetch_many(GET_SELLERS_QUERY, (product_id,))
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

    def get_quantity(self):
        while True:
            try:
                quantity = int(input("Enter the quantity: ").strip())
                if quantity > 0:
                    return quantity
                TUI.print_error("The quantity must be greater than 0.\n")
            except ValueError:
                TUI.print_error("Invalid input. Please enter a numeric value.\n")

    def get_or_create_basket(self):
        basket = self.db.fetch_one(GET_BASKET_QUERY, (self.shopper.shopper_id,))
        if not basket:
            return Basket.create_basket(self.db, self.shopper.shopper_id)
        return basket[0]

    def add_item_to_basket(self, basket_id, product_id, seller_id, quantity, price):
        self.db.exe(ADD_TO_BASKET_QUERY, (basket_id, product_id, seller_id, quantity, price))
        self.db.commit()

    def get_basket(self):
        return Basket.get_basket(self.db, self.shopper.shopper_id)

    def get_basket_contents(self, basket_id):
        return Basket.get_basket_contents(self.db, basket_id)

    def display_basket_contents(self, basket_contents):
        Basket.display_basket_contents(basket_contents)

    def select_basket_item(self, basket_contents):
        if len(basket_contents) > 1:
            while True:
                try:
                    item_no = int(input("Enter the basket item no. you want to update: ").strip())
                    if 1 <= item_no <= len(basket_contents):
                        return item_no
                    else:
                        TUI.print_error("The basket item no. you have entered is invalid.\n")
                except ValueError:
                    TUI.print_error("The basket item no. you have entered is invalid.\n")
        else:
            return 1

    def get_new_quantity(self):
        while True:
            try:
                new_quantity = int(input("Enter the new quantity of the selected product you want to buy: ").strip())
                if new_quantity > 0:
                    return new_quantity
                else:
                    TUI.print_error("The quantity must be greater than zero.\n")
            except ValueError:
                TUI.print_error("The quantity must be greater than 0.\n")

    def update_item_quantity(self, basket_id, product_id, new_quantity):
        self.db.exe(UPDATE_QUANTITY_QUERY, (new_quantity, basket_id, product_id))
        self.db.commit()

    def confirm_removal(self):
        while True:
            confirmation = input("Are you sure you want to remove this item? (Y/N): ").strip().upper()
            if confirmation in ("Y", "N"):
                return confirmation == "Y"
            TUI.print_error("Invalid input. Please enter Y or N.\n")

    def remove_item_from_basket(self, basket_id, product_id):
        self.db.exe(DELETE_ITEM_QUERY, (basket_id, product_id))
        self.db.commit()

    def confirm_checkout(self):
        while True:
            confirmation = input("Do you wish to proceed with the checkout? (Y/N): ").strip().upper()
            if confirmation in ("Y", "N"):
                return confirmation == "Y"
            TUI.print_error("Invalid input. Please enter Y or N.\n")

    def process_checkout(self, basket_id, basket_contents):
        try:
            self.db.begin_transaction()

            # Insert into shopper_orders
            self.db.exe(INSERT_ORDER_QUERY, (self.shopper.shopper_id,))
            order_id = self.db.fetch_one(GET_LAST_INSERT_ID_QUERY)[0]

            # Insert into ordered_products
            for item in basket_contents:
                product_id, _, _, quantity, price = item
                seller_id = self.db.fetch_one(
                    GET_SELLER_ID_FROM_BASKET_QUERY,
                    (basket_id, product_id)
                )[0]
                self.db.exe(INSERT_ORDERED_PRODUCT_QUERY, (order_id, product_id, seller_id, quantity, price))

            # Clear the basket
            self.db.exe(DELETE_BASKET_CONTENTS_QUERY, (basket_id,))
            self.db.exe(DELETE_SHOPPER_BASKET_QUERY, (basket_id,))

            self.db.commit()
            TUI.print_success("Checkout complete, your order has been placed.\n")
        except Exception as e:
            self.db.rollback()
            TUI.print_error(f"An error occurred during checkout: {e}\n")

if __name__ == "__main__":
    Controller("./db/parana.db")
