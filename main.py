from db import Database

class Controller:
    def __init__(self, db_path):
        self.db = Database(db_path)

if __name__ == "__main__":
    controller = Controller("./db/parana.db")

    res = controller.db.populate("./db/scripts/seller_reviews.txt")
    res = controller.db.fetch("SELECT * FROM seller_reviews;")
    print(res)
