"""Parameterized SQLite CRUD demo. The caller owns the connection lifecycle."""
import sqlite3


class InvalidItem(ValueError):
    pass


class Items:
    def __init__(self, connection):
        self.connection = connection
        connection.row_factory = sqlite3.Row
        connection.execute("CREATE TABLE IF NOT EXISTS items(id INTEGER PRIMARY KEY,name TEXT NOT NULL,description TEXT NOT NULL)")

    @staticmethod
    def validate(name, description):
        if not isinstance(name, str) or not name.strip() or len(name) > 200:
            raise InvalidItem("name must contain 1..200 characters")
        if not isinstance(description, str) or len(description) > 10000:
            raise InvalidItem("description must be a string of at most 10000 characters")

    def create(self, name, description):
        self.validate(name, description)
        with self.connection:
            return self.connection.execute("INSERT INTO items(name,description) VALUES (?,?)", (name,description)).lastrowid

    def get(self, item_id):
        row = self.connection.execute("SELECT * FROM items WHERE id=?", (item_id,)).fetchone()
        return dict(row) if row else None

    def list(self):
        return [dict(r) for r in self.connection.execute("SELECT * FROM items ORDER BY id")]

    def update(self, item_id, name, description):
        self.validate(name, description)
        with self.connection:
            return self.connection.execute("UPDATE items SET name=?,description=? WHERE id=?", (name,description,item_id)).rowcount == 1

    def delete(self, item_id):
        with self.connection:
            return self.connection.execute("DELETE FROM items WHERE id=?", (item_id,)).rowcount == 1
