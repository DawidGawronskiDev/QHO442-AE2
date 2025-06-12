import sqlite3

class Database:
    """A class to handle database operations using SQLite."""
    def __init__(self, db_path):
        """
        Initializes the Database instance with a connection to the SQLite database.
        """
        self.con = sqlite3.connect(db_path)

    def exe(self, query, args=()):
        """
        Executes a SQL query with the provided arguments.
        """
        with self.con:
            cur = self.con.cursor()
            cur.execute(query, args)
            cur.close()

    def fetch_one(self, query, args=()):
        """Fetches a single row from the database based on the provided query and arguments."""
        cur = self.con.cursor()
        cur.execute(query, args)
        row = cur.fetchone()
        cur.close()
        return row

    def fetch_many(self, query, args=()):
        """Fetches multiple rows from the database based on the provided query and arguments."""
        cur = self.con.cursor()
        cur.execute(query, args)
        rows = cur.fetchall()
        cur.close()
        return rows

    def commit(self):
        """Commits the current transaction to the database."""
        self.con.commit()

    def rollback(self):
        """Rolls back the current transaction in case of an error."""
        self.con.rollback()

    def begin_transaction(self):
        """Begins a new transaction."""
        self.con.execute("BEGIN TRANSACTION;")

    def populate(self, script_path):
        """Executes a SQL script file to populate the database."""
        with open(script_path, 'r') as file:
            script = file.read()
            statements = script.split(";")
            for statement in statements:
                if statement:
                    statement.strip()
                    self.exe(statement + ";")


    def close(self):
        self.con.close()