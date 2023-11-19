import socket
from threading import Thread

STATUS_200 = "HTTP/1.1 200 OK\r\n"
STATUS_404 = "HTTP/1.1 404 Not Found\r\n\r\n"


def handle_request(sock):
    data = sock.recv(128)
    path = get_path(data)

    headers = data.decode().strip("\r\n").split("\r\n")[1:]
    if path == "/user-agent":
        agent = ""
        for header in headers:
            if header.startswith("User-Agent"):
                agent = header.split(":")[-1].strip()

        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/plain\r\n"
            f"Content-Length: {len(agent)}\r\n\r\n"
            f"{agent}\r\n"
        )
    elif path == "/":
        response = STATUS_200 + "\r\n"
    elif path.startswith("/echo/"):
        param = path[len("/echo/") :]
        content_type = "Content-Type: text/plain\r\n"
        content_length = f"Content-Length: {len(param)}\r\n\r\n"
        content = f"{param}\r\n"
        response = STATUS_200 + content_type + content_length + content
    else:
        response = STATUS_404

    sock.send(response.encode())
    sock.close()


def get_path(data) -> str:
    request = data.decode().split("\r\n")
    head = request[0]
    path = head.split(" ")[1]
    return path


def main():
    print("Starting server:")
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        sock, _ = server_socket.accept()
        new_thread = Thread(target=handle_request, args=(sock,))
        new_thread.start()


if __name__ == "__main__":
    main()
