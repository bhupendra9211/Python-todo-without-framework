from database import get_connection

class TodoModel:
    @staticmethod
    def get_all():
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, task, completed FROM todos")
                rows = cur.fetchall()
                todos = [
                    {'id': row[0], 'task': row[1], 'completed': row[2]}
                    for row in rows
                ]
                return todos

    @staticmethod
    def create(task):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO todos (task) VALUES (%s) RETURNING id", (task,))
                conn.commit()
                return cur.fetchone()[0]

    @staticmethod
    def delete(todo_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM todos WHERE id = %s", (todo_id,))
                conn.commit()

    @staticmethod
    def toggle(todo_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE todos 
                    SET completed = NOT completed 
                    WHERE id = %s
                """, (todo_id,))
                conn.commit()
