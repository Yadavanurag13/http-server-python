import socket 
import threading
import sys

def handle_connection(sock, addr):
    req = sock.recv(1024).decode()

    path = req.split("\r\n")[0].split(" ")[1]

    if path == "/":
        sock.send(b'HTTP/1.1 200 OK\r\n\r\n')
    elif path.startswith("/echo/"):
        content = path[6:]
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(content)}\r\n\r\n{content}"
        sock.send(response.encode())
    elif path.startswith("/user-agent"):
        content = req.split(" ")[-1].split()[-1]
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(content)}\r\n\r\n{content}"
        sock.send(response.encode())
    elif path.startswith("/files"):
        directory = sys.argv[2]
        filename = path[7:]

        print(directory)
        print(filename)
        try:
            with open(f"/{directory}/{filename}", "r") as f:
                body = f.read()

                print(body)
                response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(body)}\r\n\r\n{body}"
                sock.send(response.encode())
        except:
            response = f"HTTP/1.1 404 Not Found\r\n\r\n"
            sock.send(response.encode())
    else:
        sock.send(b'HTTP/1.1 404 Not Found\r\n\r\n')
        
    sock.close()



def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        sock, add = server_socket.accept()
        thread = threading.Thread(target=handle_connection, args=(sock, add))
        thread.start()
        

if __name__ == "__main__":
    main()
