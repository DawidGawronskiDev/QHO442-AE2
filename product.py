from db import Database

class Product:
    def __init__(self):
        pass

    @staticmethod
    def get_product_categories(db: Database):
        query = """
            SELECT * FROM categories c;
        """
        rows = db.fetch_many(query)
        print(rows)

