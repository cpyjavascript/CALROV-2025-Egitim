import cv2, socket, json, os
import numpy as np

CFG_PATH = 'ai/yolov4-tiny.cfg'
WEIGHTS_PATH = 'ai/yolov4-tiny.weights'
NAMES_PATH = 'ai/coco.names'

HOST = '127.0.0.1'
PORT = 12345

net = cv2.dnn.readNet(WEIGHTS_PATH, CFG_PATH)
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

with open(NAMES_PATH, 'r') as f:
    classes = [line.strip() for line in f.readlines()]

image_files = [
    'images/image1.jpg',
    'images/image2.jpg',
    'images/image3.jpg',
    'images/image4.jpg',
    'images/image5.jpg',
    'images/image6.jpg'
]

def process_image(image_path):
    image = cv2.imread(image_path)
    height, width, _ = image.shape
    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    bounding_boxes = []
    confidences = []
    class_ids = []

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

                bounding_boxes.append([int(x), int(y), int(w), int(h)])
                confidences.append(float(confidence))
                class_ids.append(int(class_id))

    indices = cv2.dnn.NMSBoxes(bounding_boxes, confidences, score_threshold=0.5, nms_threshold=0.4)

    final_boxes = []
    if len(indices) > 0:
        for i in indices.flatten():
            final_boxes.append((*bounding_boxes[i], class_ids[i], confidences[i]))

    return final_boxes

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print("Sunucu başlatıldı, client bekleniyor...")

client_socket, addr = server_socket.accept()
print(f"Client bağlandı: {addr}")

for image_file in image_files:
    if os.path.exists(image_file):
        boxes = process_image(image_file)
        data = json.dumps(boxes)

        data_size = len(data)
        client_socket.sendall(f"{data_size:<10}".encode('utf-8'))
        
        client_socket.sendall(data.encode('utf-8'))
        print(f"{image_file} için bounding box'lar gönderildi.")
    else:
        print(f"{image_file} bulunamadı.")

client_socket.close()
server_socket.close()
