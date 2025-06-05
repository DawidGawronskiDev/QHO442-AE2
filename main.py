from db import Database

class Controller:
    def __init__(self, db_path):
        self.db = Database(db_path)

if __name__ == "__main__":
    controller = Controller("./db/parana.db")
    res = controller.db.fetch("SELECT * FROM sellers;")

    print(res)
