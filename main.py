from db import Database

class Main:
    def __init__(self, db_path):
        self.db = Database(db_path)

if __name__ == "__main__":
    main = Main("./db/parana.db")

    res = main.db.fetch("SELECT * FROM sellers;")
    print(res)