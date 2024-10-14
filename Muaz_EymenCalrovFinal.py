import cv2
import socket
import numpy as np
import pickle

Sunucu = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Sunucu.bind(("0.0.0.0", 31315))
Sunucu.listen()

print("Client beklenmekte...")

clientSocket, address = Sunucu.accept()
print(f"Client gelmiştir: {address}")

config_path = "ai/yolov4-tiny.cfg"
weights_path = "ai/yolov4-tiny.weights"
names_path = "ai/coco.names"

net = cv2.dnn.readNet(weights_path, config_path)

with open(names_path, "r") as f:
    class_names = [line.strip() for line in f.readlines()]

layers = net.getLayerNames()
output_layers = [layers[i - 1] for i in net.getUnconnectedOutLayers()]

for a in range(1, 7):
    resim = cv2.imread(f"image{a}.jpg")
    height, width = resim.shape[:2]

    blob = cv2.dnn.blobFromImage(resim, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
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


    data = pickle.dumps(boxes)

    data_sizes = len(data)
    clientSocket.sendall(pickle.dumps(data_sizes))
    clientSocket.sendall(data)

clientSocket.close()
Sunucu.close()
