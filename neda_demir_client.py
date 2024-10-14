# Gerekli kütüphaneleri yükle
import socket
import cv2
import json

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 37252))

def resim_gonder(image, conn):
    
    _, img_encoded = cv2.imencode('.jpg', image)

    
    img_bytes = img_encoded.tobytes()

    
    conn.sendall(len(img_bytes).to_bytes(4, 'big'))

    # Resim verisi yollanır
    conn.sendall(img_bytes)

def bounding_box_al(conn):
    # Bounding Box bilgileri serverdan alınır
    bounding_boxes_str = conn.recv(4096).decode('utf-8')


    bounding_boxes = json.loads(bounding_boxes_str)

    return bounding_boxes

# Örnek bir resim yükle
image = cv2.imread('images/image1.jpg')

# Resim servera yollanır
resim_gonder(image, sock)

# Serverdan tüm bounding box bilgileri alınır
bounding_boxes = bounding_box_al(sock)

# Bounding box bilgileri yazdırılır
print(f"Bounding boxes: {bounding_boxes}")

# Bağlantı kapatılır
sock.close()