# Uncomment this to pass the first stage
import socket


def main():
    print("Starting server:")
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    sock, _ = server_socket.accept()
    data = sock.recv(128)

    def get_path(data):
        request = data.decode().split("\r\n")
        head = request[0]
        path = head.split(" ")[1]
        return path

    path = get_path(data)
    if path == "/":
        sock.send(b"HTTP/1.1 200 OK\r\n\r\n")
    else:
        sock.send(b"HTTP/1.1 404 Not Found\r\n\r\n")


if __name__ == "__main__":
    main()
