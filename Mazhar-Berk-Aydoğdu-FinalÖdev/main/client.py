import socket, select

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 37252))

while True:
    isReady = select.select([sock], [], [], 1)
    
    if isReady:
        data = sock.recv(150)
        if data:
            print(str(data, "utf-8"))
        else:
            print("Bağlantı kapatıldı.")
            break