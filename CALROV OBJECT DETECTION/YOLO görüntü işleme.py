import cv2 as cv
import numpy as np
import os
import socket
# YOLOv4-tiny modelini yükle
net = cv.dnn.readNetFromDarknet("C:/Users/Lenovo PC/Desktop/CALROV OBJECT DETECTION/yolov4-tiny.cfg",
                                 "C:/Users/Lenovo PC/Desktop/CALROV OBJECT DETECTION/yolov4-tiny.weights")

# COCO sınıfları dosyasını yükle
classes = []
with open("C:/Users/Lenovo PC/Desktop/CALROV OBJECT DETECTION/coco.names", "r") as f:
    classes = f.read().strip().split('\n')

layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Resimlerin bulunduğu klasörü ayarla
image_folder = "C:/Users/Lenovo PC/Desktop/CALROV OBJECT DETECTION/images"
image_files = [f for f in os.listdir(image_folder) if f.endswith('.jpg')]

# Masaüstü yolunu bulma ve output klasörünü masaüstüne oluşturma
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
output_folder = os.path.join(desktop_path, "output")
os.makedirs(output_folder, exist_ok=True)  

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 5000))  
server_socket.listen(1)
print("Server başlatıldı, istemci bekleniyor...")

client_socket, addr = server_socket.accept()
print(f"Bağlanan istemci: {addr}")

# Her bir resmi işle
for image_file in image_files:
    image_path = os.path.join(image_folder, image_file)
    image = cv.imread(image_path)
    (h, w) = image.shape[:2]

    # YOLO için blob oluşturma
    blob = cv.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []

    # Bounding box'ları bulma ve sonuçları toplama
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * w)
                center_y = int(detection[1] * h)
                box_w = int(detection[2] * w)
                box_h = int(detection[3] * h)
                x = int(center_x - box_w / 2)
                y = int(center_y - box_h / 2)
                boxes.append([x, y, box_w, box_h])
                class_ids.append(class_id)
                confidences.append(float(confidence))

    # Non-Maximum Suppression (NMS) ile bounding box'ları temizleme
    indexes = cv.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    # Her bir bounding box için renk belirleme
    colors = np.random.uniform(0, 255, size=(len(classes), 3))

    font = cv.FONT_HERSHEY_PLAIN
    if len(indexes) > 0:
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[class_ids[i]]
            cv.rectangle(image, (x, y), (x + w, y + h), color, 2)
            cv.putText(image, label, (x, y + 30), font, 2, color, 3)

    # Sonuçları masaüstündeki output klasörüne kaydetme
    output_file = os.path.join(output_folder, f"output_{image_file}")
    cv.imwrite(output_file, image)
    print(f"Sonuç kaydedildi: {output_file}")


    bounding_boxes_str = ",".join([f"{x},{y},{w},{h}" for (x, y, w, h) in boxes])
    client_socket.sendall(bounding_boxes_str.encode('utf-8'))

client_socket.sendall("DONE".encode('utf-8'))


# Bağlantıyı kapat
client_socket.close()
server_socket.close()


            






