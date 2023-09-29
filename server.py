#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

UNACCEPTED_METHODS = ['POST', 'PUT', 'DELETE']
ROOT_PATH = 'www/'

class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        
        self.get_response(self.data)
    
    def get_response(self, data):
        data = data.decode('utf-8')
        print("data is", data)
        
        # check if there are any unpermitted methods in request
        if any(method in data for method in UNACCEPTED_METHODS):
            response = f"HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/plain;\r\n\r\n405 Try a different method"
            return self.request.sendall(bytearray(response, 'utf-8'))
        
        # parsing get request
        request_path = data.split(' ')[1]
        print("request path is", request_path)
        path = request_path[1:]
        if ROOT_PATH not in path:
            path = ROOT_PATH + path
        print("final path is", path)
        
        # handling two mime types
        content_type = ''
        if path.endswith('.html'):
            content_type = 'text/html'
        elif path.endswith('.css'):
            content_type = 'text/css'
        
        # handle dir with / and without /
        elif os.path.isdir(path):
            print(path)
            path_301 = ''.join(path.split('/')[1:])
            if not path.endswith('/'):
                path += '/'
                response = f"HTTP/1.1 301 Moved Permanantly\r\nLocation:http://127.0.0.1:8080/{path_301}/\r\nContent-Type: text/html;\r\n\r\n301 Not Found"
                self.request.sendall(bytearray(response, 'utf-8'))
                return
        
        try:
            if os.path.isdir(path):
                path += 'index.html'
                content_type = 'text/html'
            print("path in try", path)
            file = open(path, "r")
            file_content = file.read()
            file.close()
            response = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type};\r\n\r\n{file_content}"
        except:
            response = f"HTTP/1.1 404 Not FOUND\r\nContent-Type: {content_type};\r\n\r\n404 Not Found"
        self.request.sendall(bytearray(response, 'utf-8'))

        
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
