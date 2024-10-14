import socket
import pickle

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect(('127.0.0.1', 31315))

boxes = []

while True:
    data = conn.recv(4096)
    if data:
        data_boyut = pickle.loads(data)
    else:
        break

    # Veri boyutu kadar veri alalım
    data = b""
    while len(data) < data_size:
        packet = conn.recv(4096)  # 4096 byte boyutunda veri al
        if not packet:
            break
        data += packet

    # Veriyi alıp işleyelim
    if data:
        a = pickle.loads(data)
        boxes.append(a)
    else:
        break

print("Alınan kutular:", boxes)

conn.close()
