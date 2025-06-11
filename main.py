from db import Database
from tui import TUI
from shopper import Shopper

class Controller:
    def __init__(self, db_path):
        self.db = Database(db_path)
        self.shopper = None

        while True:
            self.run()

    def run(self):
        shopper_id = input("Enter Shopper ID: ").strip()
        if not shopper_id.isdigit():
            TUI.print_error("Invalid Shopper ID. Please enter a numeric value.\n")
            return

        shopper_id = int(shopper_id)

        query = f"SELECT * FROM shoppers WHERE shopper_id = {shopper_id}"
        row = self.db.fetch_one(query)
        if row is None:
            TUI.print_error("Shopper not found.\n")
            return

        self.shopper = Shopper(*row)
        self.shopper.init_basket(self.db)
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
        # i. Display a numbered list of product categories in alphabetical order
        get_categories_query = "SELECT category_id, category_description FROM categories ORDER BY category_description ASC;"
        categories = self.db.fetch_many(get_categories_query)
        if not categories:
            TUI.print_error("No product categories available.\n")
            return
        category_id = TUI.display_options(categories, "Product Categories", "category")

        # iii. Display a numbered list of products in the selected category
        get_products_query = "SELECT product_id, product_description FROM products WHERE category_id = ? ORDER BY product_description ASC;"
        products = self.db.fetch_many(get_products_query, (category_id,))
        if not products:
            TUI.print_error("No products available in this category.\n")
            return
        product_id = TUI.display_options(products, "Products", "product")

        # v. Display a numbered list of sellers for the selected product
        get_sellers_query = """
            SELECT ps.seller_id, s.seller_name, ps.price
            FROM product_sellers ps
            JOIN sellers s ON ps.seller_id = s.seller_id
            WHERE ps.product_id = ?
            ORDER BY s.seller_name ASC;
        """
        sellers = self.db.fetch_many(get_sellers_query, (product_id,))
        if not sellers:
            TUI.print_error("No sellers available for this product.\n")
            return
        seller_id = TUI.display_options(
            [(seller[0], f"{seller[1]} - ${seller[2]:.2f}") for seller in sellers],
            "Sellers",
            "seller"
        )
        price = next(seller[2] for seller in sellers if seller[0] == seller_id)

        # vii. Prompt the user to enter the quantity
        while True:
            quantity = int(input("Enter the quantity: ").strip())
            if quantity > 0:
                break
            TUI.print_error("The quantity must be greater than 0.\n")

        # viii. Check if there is a current basket, if not, create one
        get_basket_query = "SELECT basket_id FROM shopper_baskets WHERE shopper_id = ?;"
        basket = self.db.fetch_one(get_basket_query, (self.shopper.shopper_id,))
        if not basket:
            create_basket_query = "INSERT INTO shopper_baskets (shopper_id, basket_created_date_time) VALUES (?, datetime('now'));"
            self.db.exe(create_basket_query, (self.shopper.shopper_id,))
            get_last_insert_id_query = "SELECT last_insert_rowid();"
            basket_id = self.db.fetch_one(get_last_insert_id_query)[0]
        else:
            basket_id = basket[0]

        # ix. Insert the product into the basket_contents table
        add_to_basket_query = """
            INSERT INTO basket_contents (basket_id, product_id, seller_id, quantity, price)
            VALUES (?, ?, ?, ?, ?);
        """
        self.db.exe(add_to_basket_query, (basket_id, product_id, seller_id, quantity, price))

        # x. Commit the transaction
        self.db.commit()

        # xi. Print confirmation
        TUI.print_success("Item added to your basket.\n")

    def sub_3(self):
        # i. Check if there is a current basket
        get_basket_query = "SELECT basket_id FROM shopper_baskets WHERE shopper_id = ?;"
        basket = self.db.fetch_one(get_basket_query, (self.shopper.shopper_id,))
        if not basket:
            TUI.print_error("Your basket is empty.\n")
            return

        basket_id = basket[0]

        # ii. Fetch basket contents
        get_basket_contents_query = """
            SELECT bc.product_id, p.product_description, s.seller_name, bc.quantity, bc.price
            FROM basket_contents bc
            JOIN products p ON bc.product_id = p.product_id
            JOIN sellers s ON bc.seller_id = s.seller_id
            WHERE bc.basket_id = ?;
        """
        basket_contents = self.db.fetch_many(get_basket_contents_query, (basket_id,))
        if not basket_contents:
            TUI.print_error("Your basket is empty.\n")
            return

        # iii. Prepare data for display
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

        # iv. Display basket contents using TUI.print_table
        TUI.print_header("Basket Contents")
        TUI.print_table(
            (12, 64, 24, 8, 12, 12),
            ("Item No.", "Description", "Seller", "Qty", "Price", "Total"),
            rows
        )

        # v. Display total basket cost
        print(f"\nBasket Total: £{total_cost:.2f}\n")

    def sub_4(self):
        # i.
        get_basket_query = "SELECT basket_id FROM shopper_baskets WHERE shopper_id = ?;"
        basket = self.db.fetch_one(get_basket_query, (self.shopper.shopper_id,))
        if not basket:
            TUI.print_error("Your basket is empty.\n")
            return

        basket_id = basket[0]

        # Fetch basket contents
        get_basket_contents_query = """
            SELECT bc.product_id, p.product_description, s.seller_name, bc.quantity, bc.price
            FROM basket_contents bc
            JOIN products p ON bc.product_id = p.product_id
            JOIN sellers s ON bc.seller_id = s.seller_id
            WHERE bc.basket_id = ?;
        """
        basket_contents = self.db.fetch_many(get_basket_contents_query, (basket_id,))
        if not basket_contents:
            TUI.print_error("Your basket is empty.\n")
            return

        # Display current basket
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
        TUI.print_table(
            (12, 64, 24, 8, 12, 12),
            ("Item No.", "Description", "Seller", "Qty", "Price", "Total"),
            rows
        )
        print(f"\nBasket Total: £{total_cost:.2f}\n")

        # ii.
        if len(basket_contents) > 1:
            while True:
                try:
                    item_no = int(input("Enter the basket item no. you want to update: ").strip())
                    if 1 <= item_no <= len(basket_contents):
                        break
                    else:
                        TUI.print_error("The basket item no. you have entered is invalid.\n")
                except ValueError:
                    TUI.print_error("The basket item no. you have entered is invalid.\n")
        else:
            item_no = 1

        selected_item = basket_contents[item_no - 1]
        product_id = selected_item[0]

        # iii.
        while True:
            try:
                new_quantity = int(input("Enter the new quantity of the selected product you want to buy: ").strip())
                if new_quantity > 0:
                    break
                else:
                    TUI.print_error("The quantity must be greater than zero.\n")
            except ValueError:
                TUI.print_error("The quantity must be greater than 0.\n")

        # iv.
        update_quantity_query = """
            UPDATE basket_contents
            SET quantity = ?
            WHERE basket_id = ? AND product_id = ?;
        """
        self.db.exe(update_quantity_query, (new_quantity, basket_id, product_id))
        self.db.commit()

        # v.
        TUI.print_success("Quantity updated successfully.\n")
        self.sub_3()  # Reuse the basket display logic from Option 3

        # vi.
        return


if __name__ == "__main__":
    Controller("./db/parana.db")
