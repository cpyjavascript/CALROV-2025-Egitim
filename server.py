import cv2
import numpy as np
import socket
import os

# Ev dizinini bulma (Kullanıcı adını otomatik alır)
CONFIG_PATH = r'C:\ai\yolov4-tiny.cfg'
WEIGHTS_PATH = r'C:\ai\yolov4-tiny.weights'
NAMES_PATH = r'C:\ai\coco.names'


print(CONFIG_PATH)  # Yolun doğru görünüp görünmediğini kontrol et.
# Sunucu ayarları
SERVER_IP = 'localhost'
SERVER_PORT = 5000

# Nesne sınıflarını yükleme
with open(NAMES_PATH, 'r') as f:
    classes = f.read().strip().split('\n')

# YOLO modelini yükleme
net = cv2.dnn.readNet(WEIGHTS_PATH, CONFIG_PATH)

# Sunucu oluşturma ve bağlantıyı dinleme
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen(1)
print(f"Sunucu {SERVER_IP}:{SERVER_PORT} adresinde dinliyor...")

# İstemci bağlantısını kabul et
client_socket, addr = server_socket.accept()
print(f"Bağlantı sağlandı: {addr}")

# Resim klasöründeki dosyaları işleme
images_folder = 'images'
for image_file in os.listdir(images_folder):
    if image_file.endswith(('.png', '.jpg', '.jpeg')):
        image_path = os.path.join(images_folder, image_file)
        image = cv2.imread(image_path)
        height, width, _ = image.shape

        # YOLO modeline uygun formatta giriş verisi hazırlama
        blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        layer_names = net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
        outputs = net.forward(output_layers)

        boxes, confidences, class_ids = [], [], []

        # Çıktıları işleme
        for output in outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        # Non-Maximum Suppression (NMS) ile kutu filtreleme
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        # Tespit edilen kutuları listeye ekleme
        detected_boxes = []
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                detected_boxes.append([x, y, w, h])

                # Kutuları çizip nesne adlarını ekleme
                label = str(classes[class_ids[i]])
                color = (0, 255, 0)  # Yeşil renk
                cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
                cv2.putText(image, label, (x, y + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        # Kutuları istemciye gönderme
        client_socket.sendall(str(detected_boxes).encode())
        print(f"{image_file}: {detected_boxes}")

        # İşlenmiş resmi kaydetme
        output_path = os.path.join(images_folder, "output_" + image_file)
        cv2.imwrite(output_path, image)

# Bağlantıyı kapatma
client_socket.close()
server_socket.close()