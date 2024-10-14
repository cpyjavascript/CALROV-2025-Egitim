import socket
import json
import cv2
import os

HOST = '127.0.0.1'
PORT = 12345

desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
output_dir = os.path.join(desktop_path, 'improved_images')

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

image_files = [
    'images/image1.jpg',
    'images/image2.jpg',
    'images/image3.jpg',
    'images/image4.jpg',
    'images/image5.jpg',
    'images/image6.jpg'
]

def recv_all(sock, length):
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError("Veri tam alınamadı")
        data += more
    return data

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print("Sunucuya bağlandı.")

for idx, image_file in enumerate(image_files):
    try:
        data_size = int(recv_all(client_socket, 10).decode('utf-8').strip())
        data = recv_all(client_socket, data_size)

        bounding_boxes = json.loads(data.decode('utf-8'))
        print(f"Gelen bounding box'lar {image_file} için:", bounding_boxes)

        image = cv2.imread(image_file)
        if image is None:
            print(f"Resim yüklenemedi: {image_file}")
            continue

        for box in bounding_boxes:
            x, y, w, h = box
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        output_path = os.path.join(output_dir, f'improved_image{idx + 1}.jpg')
        cv2.imwrite(output_path, image)
        print(f"{output_path} kaydedildi.")

    except ValueError as e:
        print(f"Veri hatalı alındı: {e}")
        break

client_socket.close()
