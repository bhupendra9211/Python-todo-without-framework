import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST")
    )

def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS todos (
                    id SERIAL PRIMARY KEY,
                    task TEXT NOT NULL,
                    completed BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

def get_todos():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, task, completed FROM todos ORDER BY created_at")
            return cur.fetchall()

def add_todo(task):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO todos (task) VALUES (%s)", (task,))
            conn.commit()

def delete_todo(todo_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM todos WHERE id = %s", (todo_id,))
            conn.commit()

def toggle_todo(todo_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE todos 
                SET completed = NOT completed 
                WHERE id = %s
            """, (todo_id,))
            conn.commit()