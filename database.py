import psycopg2
from contextlib import contextmanager

@contextmanager
def get_connection():
    conn = psycopg2.connect(dbname="todo_db", user="postgres", password="root", host="localhost")
    try:
        yield conn
    finally:
        conn.close()
