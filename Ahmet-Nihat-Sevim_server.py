import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(("0.0.0.0", 40000))

sock.listen()

while True:
    (client, address) = sock.accept()

    with open("data.txt", "r") as file:
        client.sendall(bytes(file.read(), "utf-8"))