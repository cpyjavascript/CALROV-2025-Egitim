import socket, time, os
import cv2 as cv
import numpy as np

datas, image1_data, image2_data, image3_data, image4_data, image5_data, image6_data = [],[],[],[],[],[],[]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("0.0.0.0", 37252))
sock.listen()

def SendDatas(client_socket):
    client_socket.sendall(bytes(str(datas), "utf-8"))

client_socket, client_address = sock.accept()
print(f"{client_address} ile bağlantı kabul edildi.")

weights_path = "../ai/yolov4-tiny.weights"
cfg_path = "../ai/yolov4-tiny.cfg"
names_path = "../ai/coco.names"

with open(names_path, "r") as f:
    classes = f.read().strip().split("\n")

net = cv.dnn.readNet(weights_path, cfg_path)

net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

image_folder = "../image/"
output_folder = "../image/output/"

image_files = ["image1.jpg", "image2.jpg", "image3.jpg", "image4.jpg", "image5.jpg", "image6.jpg"]

for image_file in image_files:
    image_path = os.path.join(image_folder, image_file)
    image = cv.imread(image_path)

    if image is None:
        print(f"Resim {image_file} yüklenemedi!")
        continue

    height, width = image.shape[:2]

    blob = cv.dnn.blobFromImage(image, scalefactor=1/255.0, size=(416, 416), swapRB=True, crop=False)

    net.setInput(blob)

    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

    detections = net.forward(output_layers)

    boxes = []
    confidences = []
    class_ids = []

    for output in detections:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5:
                box = detection[0:4] * np.array([width, height, width, height])
                (centerX, centerY, w, h) = box.astype("int")

                x = int(centerX - (w / 2))
                y = int(centerY - (h / 2))

                boxes.append([x, y, int(w), int(h)])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indices = cv.dnn.NMSBoxes(boxes, confidences, score_threshold=0.5, nms_threshold=0.4)

    if len(indices) > 0:
        for i in indices.flatten():
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = confidences[i]

            if(image_file == image_files[0]):
                image1_data = ["IMAGE1 | DATA:",x,y,w,h]
            elif(image_file == image_files[1]):
                image2_data = ["IMAGE2 | DATA:",x,y,w,h]
            elif(image_file == image_files[2]):
                image3_data = ["IMAGE3 | DATA:",x,y,w,h]
            elif(image_file == image_files[3]):
                image4_data = ["IMAGE4 | DATA:",x,y,w,h]
            elif(image_file == image_files[4]):
                image5_data = ["IMAGE5 | DATA:",x,y,w,h]
            elif(image_file == image_files[5]):
                image6_data = ["IMAGE6 | DATA:",x,y,w,h]

            cv.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = f"{label}: {confidence:.2f}"
            cv.putText(image, text, (x, y - 5), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    output_path = os.path.join(output_folder, f"output_{image_file}")
    cv.imwrite(output_path, image)
    print(f"İşlenen resim kaydedildi: {output_path}")

i = 1
while i < 7:
    if(i == 1):
        datas = image1_data
    elif(i==2):
        datas = image2_data
    elif(i==3):
        datas = image3_data
    elif(i==4):
        datas = image4_data
    elif(i==5):
        datas = image5_data
    elif(i==6):
        datas = image6_data
        
    SendDatas(client_socket)
    i+=1
    time.sleep(0.1)