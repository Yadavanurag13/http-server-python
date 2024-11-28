import socket  # noqa: F401



def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    sock, add = server_socket.accept()
    sock.send(b'HTTP/1.1 200 OK\r\n\r\n')
    sock.close()
    


if __name__ == "__main__":
    main()
