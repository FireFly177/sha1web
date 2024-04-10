from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
from sha1py import sha1

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )
        message = form.getvalue('message')
        file_item = form['file'] if 'file' in form else None

        if file_item is not None and file_item.file:
            # Read file content
            message = file_item.file.read()
        else:
            # Convert string message to bytes
            message = message.encode()

        hashed_message = sha1(message)

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.send_header('Access-Control-Allow-Origin', '*')  # Allow requests from any origin
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Max-Age", "86400")
        self.end_headers()

        self.wfile.write(hashed_message.encode())

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
