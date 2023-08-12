from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import mimetypes
import socket
import pathlib
import json
from datetime import datetime

from threading import Thread

BASE_DIR = pathlib.Path()

class MainServer(BaseHTTPRequestHandler):
    def do_GET(self):
        return self.router()
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        self.send_post_data_via_socket(post_data)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response_data = json.dumps({"message": "POST request received"})
        self.wfile.write(response_data.encode('utf-8'))
    
    def send_html_file(self, filename, status=200):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())
                                
    def send_static(self, file):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header('Content-type', mt[0])
        else:
            self.send_header('Content-type', 'text/plain')
        self.end_headers()
        with open(file, 'rb') as fd:
            self.wfile.write(fd.read())
    
    
    def router(self):
        pr_url = urllib.parse.urlparse(self.path)
        
        match pr_url.path:
            case '/':
                self.send_html_file('index.html')
            case '/message':
                self.send_html_file('message.html')
            case _:
                file = BASE_DIR.joinpath(pr_url.path[1:])
                if file.exists():
                    self.send_static(file)
                else:
                    self.send_html_file('error.html', status=404)


    def send_post_data_via_socket(self, message):
        host = socket.gethostname()
        port = 5000
    
        client_socket = socket.socket()
        client_socket.connect((host, port))
        
        params = urllib.parse.parse_qs(message) # Parse the query string into a dictionary
        
        data = {
            "username": params.get("username", [""])[0],
            "message": params.get("message", [""])[0]
        }

        json_data = json.dumps(data) #Converting the dict to a JSON string. 
        
        client_socket.sendall(json_data.encode('utf-8')) #Sending the JSOn string
        
        received_data = client_socket.recv(1024).decode('utf-8')
        print(f"received message: {received_data}")
        
        client_socket.close()

                
def server_socket():
    print("Socket start listening")
    host = socket.gethostname()
    port = 5000
    
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(2)
    conn, address = server_socket.accept()
    print(f"Connection from {address}")
    while True:
        post_data = conn.recv(1024).decode('utf-8')
        if not post_data:
            break
        print(f'received message: {post_data}')
        
        try:
            data = json.loads(post_data) #Converting a string to a dictionary
            print("Decoded JSON data:", data)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            data['timestamp'] = timestamp
            with open('storage/data.json', 'r+') as f:
                stored_data = json.load(f) if f.readable() else {}
                stored_data[timestamp] = data
                f.seek(0)
                json.dump(stored_data, f, indent=2)
            print("Data successfully saved to data.json. ")
        except json.JSONDecodeError:
            print("Received data is not a valid JSON. ")
            
    conn.close()

               
def run(server_class=HTTPServer, handler_class=MainServer):
    server_adress = ('', 3000)
    http = server_class(server_adress, handler_class)
    try:
        print("Start running...")
        socket_sever = Thread(target=server_socket)
        socket_sever.start()
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()
        
run()