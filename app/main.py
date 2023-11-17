import socket
import re


def get_path(data) -> str:
    request = data.decode().split("\r\n")
    head = request[0]
    path = head.split(" ")[1]
    return path


STATUS_200 = "HTTP/1.1 200 OK\r\n\r\n"
STATUS_404 = "HTTP/1.1 404 Not Found\r\n\r\n"


def main():
    print("Starting server:")
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    sock, _ = server_socket.accept()
    data = sock.recv(128)

    path = get_path(data)

    if path == "/":
        response = STATUS_200
        sock.send(response.encode())
        sock.close()
        return

    regex = re.compile(r"/echo/(.+$)")
    match = regex.match(path)
    if not match:
        response = STATUS_404
        sock.send(response.encode())
        sock.close()
    else:
        param = match.group(1)
        body = f"Content-Type: text/plain\r\n{param}\r\n"
        response = STATUS_200 + body
        sock.send(response.encode())
        sock.close()
        return


if __name__ == "__main__":
    main()
