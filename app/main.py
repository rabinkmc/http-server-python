import socket
import re


def get_path(data) -> str:
    request = data.decode().split("\r\n")
    head = request[0]
    path = head.split(" ")[1]
    return path


STATUS_200 = "HTTP/1.1 200 OK\r\n"
STATUS_404 = "HTTP/1.1 404 Not Found\r\n\r\n"


def main():
    print("Starting server:")
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    sock, _ = server_socket.accept()
    data = sock.recv(128)

    path = get_path(data)

    if path == "/user-agent":
        headers = data.decode().strip("\r\n").split("\r\n")[1:]
        agent = ""
        for header in headers:
            if header.startswith("User-Agent"):
                agent = header

        agent = agent.split(":")[-1].strip()
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/plain\r\n"
            f"Content-Length: {len(agent)}\r\n\r\n"
            f"{agent}\r\n"
        )
        sock.send(response.encode())

    elif path == "/":
        response = STATUS_200 + "\r\n"
        sock.send(response.encode())

    elif match := re.match(r"/echo/(.+$)", path):
        param = match.group(1)
        content_type = "Content-Type: text/plain\r\n"
        content_length = f"Content-Length: {len(param)}\r\n\r\n"
        content = f"{param}\r\n"
        response = STATUS_200 + content_type + content_length + content
        sock.send(response.encode())
    else:
        response = STATUS_404
        sock.send(response.encode())
    sock.close()


if __name__ == "__main__":
    main()
