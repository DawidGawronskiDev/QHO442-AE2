from utils.Database import Database

class Tester:
    def __init__(self, db_path):
        self.db = Database(db_path)
        self.run()

    def populate(self):
        scripts = (
            "./../db/scripts/product_reviews.txt",
            "./../db/scripts/seller_reviews.txt",
            "./../db/scripts/product_discounts.txt"
        )
        for script in scripts:
            try:
                self.db.populate(script)
                print("Database populated successfully.")
            except Exception as e:
                print(f"Error populating database with script {script}: {e}")

    def run(self):
        self.populate()

        print("\nTesting product reviews table:")
        rows = self.db.fetch_many("SELECT * FROM product_reviews LIMIT 10;")
        for row in rows:
            print(row)

        print("\nTesting seller reviews table:")
        rows = self.db.fetch_many("SELECT * FROM seller_reviews LIMIT 10;")
        for row in rows:
            print(row)

        print("\nTesting product discounts table:")
        rows = self.db.fetch_many("SELECT * FROM product_discounts LIMIT 10;")
        for row in rows:
            print(row)


def main():
    Tester("./../db/parana.db")

if __name__ == "__main__":
    main()