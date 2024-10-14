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

    data = b""
    while len(data) < data_size:
        packet = conn.recv(4096)
        if not packet:
            break
        data += packet

    if data:
        a = pickle.loads(data)
        boxes.append(a)
    else:
        break

print("Taken Boxes:", boxes)

conn.close()
