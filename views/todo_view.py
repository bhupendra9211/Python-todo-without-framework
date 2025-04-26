import json

class TodoView:
    @staticmethod
    def render_html():
        with open('templates/index.html', 'r') as file:
            return file.read()

    @staticmethod
    def render_json(todos):
        return json.dumps(todos)

    @staticmethod
    def redirect_home():
        return None  # Your server logic will handle this (sending 303 response)
