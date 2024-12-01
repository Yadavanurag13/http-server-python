import socket 
import threading
import sys

def handle_connection(sock, addr):
    req = sock.recv(1024).decode()
    path = req.split("\r\n")[0].split(" ")[1]

    encoding = req.split("\r\n")[-3].split(":")[0]
    encoding_type = req.split("\r\n")[-3].split(":")[1].strip()

    str = req.split("\r\n")[-3].split(":")[1]

    print(req)
    print(path)

    print(encoding)

    print(type(list))
    if path == "/":
        sock.send(b'HTTP/1.1 200 OK\r\n\r\n')

    elif path.startswith("/echo/"):
        if encoding == "Accept-Encoding":
            if "gzip" in str:
                content = path[6:]
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Encoding: gzip\r\nContent-Length: {len(content)}\r\n\r\n{content}"

                sock.send(response.encode())
            else:
                content = path[6:]
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(content)}\r\n\r\n{content}"
                sock.send(response.encode())
        else:
            content = path[6:]
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(content)}\r\n\r\n{content}"
            sock.send(response.encode())

    elif path.startswith("/user-agent"):

        if encoding == "Accept-Encoding":
            if "gzip" in str:
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Encoding: gzip\r\nContent-Length: {len(content)}\r\n\r\n{content}"

                sock.send(response.encode())
            else:
                content = path[6:]

                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(content)}\r\n\r\n{content}"

                sock.send(response.encode())
        else:
            content = req.split(" ")[-1].split()[-1]
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(content)}\r\n\r\n{content}"
            sock.send(response.encode())

    elif path.startswith("/files"):

        method = req.split("\r\n")[0].split(" ")[0]

        if method == "GET":
            directory = sys.argv[2]
            filename = path[7:]

            try:
                with open(f"/{directory}/{filename}", "r") as f:
                    body = f.read()

                    # print(body)
                    response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(body)}\r\n\r\n{body}"
                    sock.send(response.encode())
            except:
                response = f"HTTP/1.1 404 Not Found\r\n\r\n"
                sock.send(response.encode())
        
        if method == "POST":
            directory = sys.argv[2]
            filename = path[7:]

            body = req.split("\r\n\r\n")[1]

            print(method, directory, filename, body)
            try:
                file_path = f"{directory}/{filename}"
                with open(file_path, "w") as filename:
                    filename.write(body)

                response = f"HTTP/1.1 201 Created\r\n\r\n"
                sock.send(response.encode())
            except:
                pass
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
