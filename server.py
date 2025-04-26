from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import database
import urllib.parse
import json

class Handler(BaseHTTPRequestHandler):
    # GET Requests
    def do_GET(self):
        if self.path == '/':
            self.send_html('templates/index.html')
        elif self.path == '/todos':
            self.send_json_todos()
        else:
            if self.path.endswith('.css'):
                self.serve_static('text/css', self.path.lstrip('/'))
            elif self.path.endswith('.js'):
                self.serve_static('application/javascript', self.path.lstrip('/'))
            elif self.path.endswith('.png'):
                self.serve_static('image/png', self.path.lstrip('/'))
            elif self.path.endswith('.jpg') or self.path.endswith('.jpeg'):
                self.serve_static('image/jpeg', self.path.lstrip('/'))
            else:
                self.send_error(404, "File not found")


    
    # POST Requests
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode()
        data = urllib.parse.parse_qs(post_data)
        
        if self.path == '/add':
            database.add_todo(data['task'][0])
        elif self.path == '/delete':
            database.delete_todo(data['id'][0])
        elif self.path == '/toggle':
            database.toggle_todo(data['id'][0])
        
        self.send_response(303)
        self.send_header('Location', '/')
        self.end_headers()

    # Helper methods
    def send_html(self, file_path):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(file_path, 'rb') as f:
            self.wfile.write(f.read())

    def send_json_todos(self):
        todos = [{
            'id': todo[0],
            'task': todo[1],
            'completed': todo[2]
        } for todo in database.get_todos()]
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(todos).encode())

    def serve_static(self, content_type, file_path):
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.end_headers()
        with open(file_path, 'rb') as file:
            self.wfile.write(file.read())
    
if __name__ == '__main__':
    database.init_db()
    PORT = 8000
    server = HTTPServer(('', PORT), Handler)
    print(f"Server running on port {PORT}")
    server.serve_forever()
