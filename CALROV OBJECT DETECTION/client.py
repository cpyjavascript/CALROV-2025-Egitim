import socket

# İstemci oluştur
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Server'a bağlan
client_socket.connect(('127.0.0.1', 12353))  # Server IP adresi ve portu

# Server'dan gelen bounding box verilerini al
data = client_socket.recv(4096).decode('utf-8')  # Veriyi al ve decode et

# Gelen verileri ekrana yazdır
print("Gelen bounding box verileri (x, y, w, h):")
bounding_boxes = data.split(",")
for i in range(0, len(bounding_boxes), 4):
    x, y, w, h = bounding_boxes[i:i+4]
    print(f"x: {x}, y: {y}, w: {w}, h: {h}")

# Bağlantıyı kapat
client_socket.close()  

