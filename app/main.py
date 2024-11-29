import socket  # noqa: F401



def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    sock, add = server_socket.accept()

    req = sock.recv(1024).decode()

    print(req)
    method = req.split("\r\n")[0].split(" ")[1]

    # str = req.split("\r\n")[0].split(" ")[1].split("/")[2]
    # print(str)

    # sock.send(b'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 3\r\n\r\n{str}')

    if method == "/":
        sock.send(b'HTTP/1.1 200 OK\r\n\r\n')
    else:
        sock.send(b'HTTP/1.1 404 Not Found\r\n\r\n')

    sock.close()



if __name__ == "__main__":
    main()
