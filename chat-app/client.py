import socket, time, threading

username = input("Enter username: ")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 37252))

sock.sendall(bytes(f"My username is: {username}", "utf-8"))

def terminal_input():
    while True:
        message = input()
        sock.sendall( bytes(f"This is a message: {message}", "utf-8"))

threading.Thread(target=terminal_input).start()

while True:
    print(str(sock.recv(150), "utf-8"))
