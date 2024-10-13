import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(("127.0.0.1", 41698))

while True:
    message = str(sock.recv(250), "utf-8")

    print(message)