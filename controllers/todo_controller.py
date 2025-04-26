from models.todo_model import TodoModel
from views.todo_view import TodoView

class TodoController:
    @staticmethod
    def handle_get(path):
        if path == '/todos':
            todos = TodoModel.get_all()
            return TodoView.render_json(todos)
        else:
            return TodoView.render_html()

    @staticmethod
    def handle_post(path, data):
        if path == '/add':
            TodoModel.create(data['task'][0])
        elif path == '/delete':
            TodoModel.delete(data['id'][0])
        elif path == '/toggle':
            TodoModel.toggle(data['id'][0])
        return None  # Redirect logic is handled by server
