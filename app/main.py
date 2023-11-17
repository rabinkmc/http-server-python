# Uncomment this to pass the first stage
import socket


def main():
    print("Starting server:")
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    def get_path(data):
        request = data.decode().split("\r\n")
        head = request[0]
        path = head.split(" ")[1]
        return path

    sock, _ = server_socket.accept()
    data = sock.recv(128)

    path = get_path(data)
    echo = path.split("/")[-1]
    response = f"HTTP/1.1 200 OK\r\n\r\nContent-Type: text/plain\r\n{echo}\r\n"
    sock.send(response.encode())
    sock.close()


if __name__ == "__main__":
    main()
