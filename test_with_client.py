import socket

BYTES_TO_READ = 4096

URL = "127.0.0.1"

def get(host, port):
    request = "GET / HTTP/1.1\nHost: " + "127.0.0.1/www/iandex.html" + "\n\n"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall(request.encode())
    s.shutdown(socket.SHUT_WR)
    result = b''
    while True:
        data = s.recv(BYTES_TO_READ)
        if not data:
            break
        result += data
    print(result)
    s.close()
    
get(URL, 8001)
