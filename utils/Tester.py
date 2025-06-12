from utils.Database import Database
from utils.TUI import TUI
from utils.Table import Table
import sqlite3

class Tester:
    def __init__(self, db_path):
        self.db = Database(db_path)
        self.db.con.row_factory = sqlite3.Row  # nicer row output
        self.run()

    def populate(self):
        scripts = (
            "./../db/scripts/product_reviews.txt",
            "./../db/scripts/seller_reviews.txt",
            "./../db/scripts/product_discounts.txt"
        )
        for script in scripts:
            try:
                print(f"Populating database with script: {script}")
                self.db.populate(script)
                print("Database populated successfully.\n")
            except Exception as e:
                print(f"Error populating database with script {script}: {e}\n")

    # Successful tests
    def test_product_reviews(self):
        query = "SELECT review_id, product_id, shopper_id, star_rating, review_comment, DATE(review_date) FROM product_reviews LIMIT 10;"
        print("Test: Fetch first 10 rows from product_reviews")
        print("Query:", query)
        try:
            rows = self.db.fetch_many(query)
            Table(
                (16, 16, 16, 16, 32, 16),
                ("review_id", "product_id", "review_text", "rating", "review_date", "reviewer_name"),
                rows
            ).print_table()
            TUI.print_success("Test passed ✅\n")
        except Exception as e:
            TUI.print_error(f"Test failed ❌: {e}\n")

    def test_seller_reviews(self):
        query = "SELECT review_id, seller_id, shopper_id, star_rating, review_comment, DATE(review_date) FROM seller_reviews LIMIT 10;"
        print("Test: Fetch first 10 rows from seller_reviews")
        print("Query:", query)
        try:
            rows = self.db.fetch_many(query)
            Table(
                (16, 16, 16, 16, 32, 16),
                ("review_id", "seller_id", "shopper_id", "star_rating", "review_comment", "review_date"),
                rows
            ).print_table()
            TUI.print_success("Test passed ✅\n")
        except Exception as e:
            TUI.print_error(f"Test failed ❌: {e}\n")

    def test_product_discounts(self):
        query = "SELECT discount_id, product_id, discount_percentage, DATE(end_date) FROM product_discounts LIMIT 10;"
        print("Test: Fetch first 10 rows from product_discounts")
        print("Query:", query)
        try:
            rows = self.db.fetch_many(query)
            Table(
                (16, 16, 24, 16),
                ("discount_id", "product_id", "discount_percentage", "end_date"),
                rows
            ).print_table()
            TUI.print_success("Test passed ✅\n")
        except Exception as e:
            TUI.print_error(f"Test failed ❌: {e}\n")

    # Intentionally failing tests
    def test_fail_product_reviews(self):
        query = "SELECT * FROM product_reviews_wrong_table LIMIT 10;"
        print("Test: Intentionally failing query on product_reviews (wrong table)")
        print("Query:", query)
        try:
            rows = self.db.fetch_many(query)
            print(f"Fetched {len(rows)} rows:")
            for row in rows:
                print(dict(row))
            TUI.print_error("Test unexpectedly passed ❌\n")
        except Exception as e:
            TUI.print_success(f"Expected failure caught ✅: {e}\n")

    def test_fail_seller_reviews(self):
        query = "SELECT non_existing_column FROM seller_reviews LIMIT 10;"
        print("Test: Intentionally failing query on seller_reviews (non-existing column)")
        print("Query:", query)
        try:
            rows = self.db.fetch_many(query)
            print(f"Fetched {len(rows)} rows:")
            for row in rows:
                print(dict(row))
            TUI.print_error("Test unexpectedly passed ❌\n")
        except Exception as e:
            TUI.print_success(f"Expected failure caught ✅: {e}\n")

    def test_fail_product_discounts(self):
        query = "INSERT INTO product_discounts (product_id, discount_percentage, end_date) VALUES (1, 150, '2025-12-31');"
        print("Test: Intentionally failing INSERT on product_discounts (invalid discount_percentage > 100)")
        print("Query:", query)
        try:
            self.db.exe(query)
            TUI.print_error("Test unexpectedly passed ❌\n")
        except Exception as e:
            TUI.print_success(f"Expected failure caught ✅: {e}\n")

    def test_insert_valid_product_reviews(self):
        query = """
        INSERT INTO product_reviews (product_id, shopper_id, star_rating, review_comment, review_date)
        VALUES (3000000, 10000, 5, 'Excellent product!', DATE('now'));
        """
        print("Test: Insert valid data into product_reviews")
        print("Query:", query)
        try:
            self.db.exe(query)
            TUI.print_success("Valid insert test passed ✅\n")
        except Exception as e:
            TUI.print_error(f"Valid insert test failed ❌: {e}\n")

    def test_insert_invalid_product_reviews(self):
        query = """
        INSERT INTO product_reviews (product_id, shopper_id, star_rating, review_comment, review_date)
        VALUES (3000000, 10000, 6, 'Invalid rating!', DATE('now'));
        """
        print("Test: Intentionally fail insert into product_reviews (invalid star_rating > 5)")
        print("Query:", query)
        try:
            self.db.exe(query)
            TUI.print_error("Test unexpectedly passed ❌\n")
        except Exception as e:
            TUI.print_success(f"Expected failure caught ✅: {e}\n")

    def test_insert_invalid_product_discounts(self):
        query = """
        INSERT INTO product_discounts (product_id, discount_percentage, end_date)
        VALUES (3000000, 150, '2025-12-31');
        """
        print("Test: Intentionally fail insert into product_discounts (invalid discount_percentage > 100)")
        print("Query:", query)
        try:
            self.db.exe(query)
            TUI.print_error("Test unexpectedly passed ❌\n")
        except Exception as e:
            TUI.print_success(f"Expected failure caught ✅: {e}\n")

    def run(self):
        self.populate()

        # Successful tests
        self.test_product_reviews()
        self.test_seller_reviews()
        self.test_product_discounts()

        # Failure tests
        self.test_fail_product_reviews()
        self.test_fail_seller_reviews()
        self.test_fail_product_discounts()

        # New tests
        self.test_insert_valid_product_reviews()
        self.test_insert_invalid_product_reviews()
        self.test_insert_invalid_product_discounts()

def main():
    Tester("./../db/parana.db")

if __name__ == "__main__":
    main()
