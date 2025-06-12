import sqlite3

class Database:
    def __init__(self, db_path):
        self.con = sqlite3.connect(db_path)

    def exe(self, query, args=()):
        with self.con:
            cur = self.con.cursor()
            cur.execute(query, args)
            cur.close()

    def fetch_one(self, query, args=()):
        cur = self.con.cursor()
        cur.execute(query, args)
        row = cur.fetchone()
        cur.close()
        return row

    def fetch_many(self, query, args=()):
        cur = self.con.cursor()
        cur.execute(query, args)
        rows = cur.fetchall()
        cur.close()
        return rows

    def commit(self):
        self.con.commit()

    def rollback(self):
        self.con.rollback()

    def begin_transaction(self):
        self.con.execute("BEGIN TRANSACTION;")

    def populate(self, script_path):
        with open(script_path, 'r') as file:
            script = file.read()
            statements = script.split(";")
            for statement in statements:
                if statement:
                    statement.strip()
                    self.exe(statement + ";")


    def close(self):
        self.con.close()