import sqlite3


class DatabaseHandler:
    """
    This is used to interact with the database.
    """
    def __init__(self, db_path='merchendise.db'):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def execute_query(self, query, parameters=None):
        with self.connection:
            if parameters:
                self.cursor.execute(query, parameters)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()

    def commit_changes(self):
        self.connection.commit()

    def create_tables(self):
        sql = """
        CREATE TABLE IF NOT EXISTS"Stock" (
            "id"	INTEGER NOT NULL UNIQUE,
            "name"	TEXT,
            "price"	REAL,
            "quantity"	INTEGER,
            "musicGroup"	TEXT,
            PRIMARY KEY("id" AUTOINCREMENT)
            );
            """
        self.execute_query(sql)
        sql = """
        CREATE TABLE IF NOT EXISTS "Sales" (
            "id"	INTEGER NOT NULL UNIQUE,
            "itemid"	INTEGER,
            "date"	TEXT,
            PRIMARY KEY("id" AUTOINCREMENT)
            );
        """
        self.execute_query(sql)
        self.commit_changes()
