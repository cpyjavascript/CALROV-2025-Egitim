import socket
import json
import cv2
import os

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 5000

output_folder = 'detected_output'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Kullanıcıdan resim dosyalarının yollarını alma
images = [
    'images/image1.jpg',
    'images/image2.jpg',
    'images/image3.jpg',
    'images/image4.jpg',
    'images/image5.jpg',
    'images/image6.jpg'
]

def receive_complete_data(sock, expected_length):
    complete_data = b''
    while len(complete_data) < expected_length:
        chunk = sock.recv(expected_length - len(complete_data))
        if not chunk:
            raise ConnectionError("Sunucudan veri alınamadı")
        complete_data += chunk
    return complete_data

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_ADDRESS, SERVER_PORT))
print("Sunucuya bağlandım.")

for img_path in images:
    try:
        size_info = int(receive_complete_data(client_socket, 10).decode('utf-8').strip())
        raw_data = receive_complete_data(client_socket, size_info)

        detected_boxes = json.loads(raw_data.decode('utf-8'))
        print(f"{img_path} için tespit edilen kutular:", detected_boxes)

        image = cv2.imread(img_path)
        if image is None:
            print(f"Resim açılamadı: {img_path}")
            continue

        for box in detected_boxes:
            x, y, w, h = box
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        result_image_path = os.path.join(output_folder, os.path.basename(img_path))
        cv2.imwrite(result_image_path, image)
        print(f"Sonuç resmi kaydedildi: {result_image_path}")

    except ValueError as e:
        print(f"Veri alımında hata: {e}")
        break

client_socket.close()
