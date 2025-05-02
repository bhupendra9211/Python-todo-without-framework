from http.server import BaseHTTPRequestHandler, HTTPServer
from routes.todo_routes import TodoRoutes
import os

class TodoServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/static/'):
            self.serve_static()
        else:
            response = TodoRoutes.route(self)
            if response is None:
                self.send_response(303)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Location', '/')
                self.end_headers()
            elif self.path == '/todos':
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(response.encode())
            else:
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                self.wfile.write(response.encode())

    def do_POST(self):
        response = TodoRoutes.route(self)
        self.send_response(303)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Location', '/')
        self.end_headers()

    def do_OPTIONS(self): 
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def serve_static(self):
        filepath = self.path.lstrip('/')
        if os.path.isfile(filepath):
            if filepath.endswith('.css'):
                content_type = 'text/css'
            elif filepath.endswith('.js'):
                content_type = 'application/javascript'
            else:
                content_type = 'application/octet-stream'
            
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', content_type)
            self.end_headers()
            with open(filepath, 'rb') as file:
                self.wfile.write(file.read())
        else:
            self.send_error(404, "File not found")

if __name__ == "__main__":
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, TodoServer)
    print("Server running at http://localhost:8000")
    httpd.serve_forever()
