
import argparse
import time
import cv2 
import numpy as np
import socket
detected=[]

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type=str, default="", required=False,
	help="path to input image file")
parser.add_argument("-o", "--output", type=str, default="",
	help="path to (optional) output image file. Write only the name, without extension.")
parser.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
parser.add_argument("-t", "--threshold", type=float, default=0.4,
	help="threshold for non maxima supression")

args = parser.parse_args()

CONFIDENCE_THRESHOLD = args.confidence
NMS_THRESHOLD = args.threshold
#Buraya istedğimiz dosyanın path ini ekliyorum
impath = r"C:\Users\PC\Desktop\ata.verdi.py\ata.verdi.py\image2.jpg"

with open(r"C:\Users\PC\Desktop\ata.verdi.py\Yolo\coco.names" , "r") as file:
    classes = file.read().strip().split("\n")

weights = r"C:\Users\PC\Desktop\ata.verdi.py\Yolo\odev\yolov4-tiny.weights" 
labels = r"C:\Users\PC\Desktop\ata.verdi.py\Yolo\odev\coco.names"
cfg = r"C:\Users\PC\Desktop\ata.verdi.py\Yolo\odev\yolov4-tiny.cfg" 

print("Kullanılıyor: {} weights ,{} configs and {} labels.".format(weights, cfg, labels))

labls = list()
with open(labels, "r") as f:
    labls = [c.strip() for c in f.readlines()]

COLORS = np.random.randint(0, 255, size=(len(labls), 3), dtype="uint8")

net = cv2.dnn.readNetFromDarknet(cfg, weights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

layer = net.getLayerNames()
layer = [layer[i - 1] for i in net.getUnconnectedOutLayers()]


def detect(imgpath, nn):
    image = cv2.imread(imgpath)
    assert image is not None, f"Lütfen dosya giriniz: {imgpath}"

    (H, W) = image.shape[:2]

    blob = cv2.dnn.blobFromImage(image, 1 / 255, (416, 416), swapRB=True, crop=False)
    nn.setInput(blob)
    start_time = time.time()
    layer_outs = nn.forward(layer)
    end_time = time.time()

    boxes = list()
    confidences = list()
    class_ids = list()

    for output in layer_outs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > CONFIDENCE_THRESHOLD:
                box = detection[0:4] * np.array([W, H, W, H])
                (center_x, center_y, width, height) = box.astype("int")

                x = int(center_x - (width / 2))
                y = int(center_y - (height / 2))

                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    idexs = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
    if len(idexs) > 0:
        for i in idexs.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])

            color = [int(c) for c in COLORS[class_ids[i]]]
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            text = "{}: {:.4f}".format(lbls[class_ids[i]], confidences[i])
            cv2.putText(
                image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2
            )
            label = "Inference Time: {:.2f} s".format(end_time - start_time)
            cv2.putText(
                image, label, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2
            )
        if len(idexs) > 0:
            for i in idexs.flatten():
                x, y, w, h = boxes[i]

                detected.append({
                    'class_name' : classes[class_ids[i]],
                    'class_id' : class_ids[i],
                    'box' : [x, y, w, h]
                })
                
         
          
    cv2.imshow("image", image)
    cv2.imwrite("yenifoto.png",image)
    if args.output != "":
        cv2.imwrite(args.output, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
detect(impath, net)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(("0.0.0.0", 41699))

sock.listen()

while True:
    (client, address) = sock.accept()
    for s in detected:
     client.sendall(bytes(s, "utf-8"))



