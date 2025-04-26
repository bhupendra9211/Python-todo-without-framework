from controllers.todo_controller import TodoController
from urllib.parse import parse_qs

class TodoRoutes:
    @staticmethod
    def route(request):
        path = request.path
        method = request.command

        if method == 'GET':
            return TodoController.handle_get(path)
        elif method == 'POST':
            content_length = int(request.headers.get('Content-Length', 0))
            post_data = request.rfile.read(content_length).decode()
            data = parse_qs(post_data)
            return TodoController.handle_post(path, data)
