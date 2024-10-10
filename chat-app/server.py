import socket, threading

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(("0.0.0.0", 37252))

sock.listen()

connected_clients = []

def handle_client(client_sock, address):
    while True:
        data = client_sock.recv(100)
        if not data:
            break
        data_str = str(data, "utf-8")
        if data_str.startswith("My username is:"):
            username = data_str[len("My username is: "):]
            print(f"Bu kullaıncının adı: {username}")
        elif data_str.startswith("This is a message: "):
            for connected_client in connected_clients:
                if connected_client == client_sock:
                    continue
                message = data_str[len("My message is: "):]
                connected_client.sendall(bytes(f"{username}: {message}", "utf-8"))

        

        

while True:
    (client_sock, address) = sock.accept()
    connected_clients.append(client_sock)
    threading.Thread(target=handle_client, args=(client_sock, address)).start()
    