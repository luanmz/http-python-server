import socket

HOST = "0.0.0.0"
PORT = 5002

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((HOST, PORT))

server_socket.listen(5)

print(f"Listening on port: {PORT} ...")

try:
    while True:

        client_socket, client_address = server_socket.accept()

        try:
            request = client_socket.recv(1500).decode()
        except:
            try:
                request = client_socket.recv(1500).decode("latin-1")
            except:
                response = 'HTTP/1.1 400 Bad Request\r\n\r\n'
                client_socket.sendall(response.encode())
                client_socket.close()
                continue
        
        try:
            request_elements, request_body = request.split("\r\n\r\n", 1)
        except:
            response = 'HTTP/1.1 400 Bad Request\r\n\r\n'
            client_socket.sendall(response.encode())
            client_socket.close()
            continue
            
        
        request_elements = request.split("\r\n")
        request_line = request_elements[0].split()
        request_headers = request_elements[1:]
        
        print(request_headers, request_body)

        if len(request_line) < 3 or not request.__contains__("\r\n\r\n"):
            response = 'HTTP/1.1 400 Bad Request\r\n\r\n'
        else:
            http_method = request_line[0]
            path = request_line[1]
            bad_request = False


            headers = {}
            for header in request_headers:
                if ": " in header:
                    key, value = header.split(": ", 1)
                    headers[key] = value
                else:
                   bad_request == True
                   break
            
            print(headers)
                   
            
            if bad_request or 'Host' not in headers:
                response = 'HTTP/1.1 400 Bad Request\r\n\r\n'
            elif http_method == "GET":
                if path == '/':
                    fin = open('index.html')
                    content = fin.read()
                    fin.close()
                    response = 'HTTP/1.1 200 OK\r\n\r\n' + content
                else:
                    response = 'HTTP/1.1 404 Not Found\r\n\r\n'
            else:
                response = 'HTTP/1.1 405 Method Not Allowed\r\nAllow: GET\r\n\r\n'

        client_socket.sendall(response.encode())
        client_socket.close()
except KeyboardInterrupt:
    print("\nServer turned off.")