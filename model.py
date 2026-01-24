from nicegui import binding
import sqlite3
import pandas as pd


@binding.bindable_dataclass
class Book:
    title: str
    rating: int


def db_init():
    with sqlite3.connect("TEST.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                rating ITNEGER NOT NULL);
        """)


def view():
    with sqlite3.connect("TEST.db") as conn:
        df = pd.read_sql_query("SELECT * FROM books", conn)
        return df


def submit(book):
    with sqlite3.connect("TEST.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO books (title, rating)
            VALUES (?, ?)
        """,
            (book.title, book.rating),
        )
