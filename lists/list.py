import os

from contextlib import closing
import json

from database import sqlite

"""
An implementation of a list that uses SQLite as a backend.

We use SQLite for 2 reasons: firstly, it's native to Python, and secondly, it's lightweight and easy to use.    
"""


class List:
    def __init__(self, name):
        self.name = name
        self.create_table_if_not_exists()
        # create the path ./generated/lists to avoid errors
        self.dump_to_json(f"./generated/lists/{name}.json")

    def create_table_if_not_exists(self):
        with closing(sqlite.connection.cursor()) as cursor:
            cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {self.name} (id INTEGER PRIMARY KEY, name TEXT)"
            )
            sqlite.connection.commit()

    def add(self, value):
        with closing(sqlite.connection.cursor()) as cursor:
            cursor.execute(f"INSERT INTO {self.name} (name) VALUES (?)", (value,))
            sqlite.connection.commit()
            self.dump_to_json(f"./generated/lists/{self.name}.json")

    def get_all(self):
        with closing(sqlite.connection.cursor()) as cursor:
            cursor.execute(f"SELECT * FROM {self.name}")
            return cursor.fetchall()

    def remove(self, value):
        with closing(sqlite.connection.cursor()) as cursor:
            cursor.execute(f"DELETE FROM {self.name} WHERE name = ?", (value,))
            sqlite.connection.commit()
            self.dump_to_json(f"./generated/lists/{self.name}.json")

    def exists(self, value):
        with closing(sqlite.connection.cursor()) as cursor:
            cursor.execute(f"SELECT * FROM {self.name} WHERE name = ?", (value,))
            return cursor.fetchone() is not None

    def add_many(self, values):
        with closing(sqlite.connection.cursor()) as cursor:
            cursor.executemany(f"INSERT INTO {self.name} (name) VALUES (?)", values)
            sqlite.connection.commit()
            self.dump_to_json(f"./generated/lists/{self.name}.json")

    def count(self):
        with closing(sqlite.connection.cursor()) as cursor:
            cursor.execute(f"SELECT COUNT(*) FROM {self.name}")
            return cursor.fetchone()[0]

    def to_array(self):
        with closing(sqlite.connection.cursor()) as cursor:
            cursor.execute(f"SELECT * FROM {self.name}")
            return [row[1] for row in cursor.fetchall()]

    def dump_to_json(self, filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as file:
            r = json.dumps(self.to_array())
            file.write(r)
