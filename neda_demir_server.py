#Gerekli kütüphaneleri yüklüyoruz.
import socket
import cv2
import numpy as np
import json


# YOLOv4-tiny model'ini yüklüyoruz
net = cv2.dnn.readNet("ai/yolov4-tiny.weights", "ai/yolov4-tiny.cfg")

# Soket bağlantısı kuruluyor
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Dinlenecek ip ve port ayarlanıyor
sock.bind(("0.0.0.0", 37252))

sock.listen()



def resim_al(conn):
    # Receive image size first (4 bytes)
    img_size = int.from_bytes(conn.recv(4), 'big')

    # Receive the image data based on its size
    img_data = b''
    while len(img_data) < img_size:
        packet = conn.recv(4096)
        if not packet:
            break
        img_data += packet

    # Convert the received data to a numpy array and decode it as an image
    nparr = np.frombuffer(img_data, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    return image


def bounding_box_bul(image):
    # İmajın yükseklik ve genişlik değerlerini alıyoruz.
    h, w = image.shape[:2]
    #İmaj bazı ön işlemelerden geçirilerek Blob formatına dönüştürülür.
    #İmaj bazı ön işlemelerden geçirilerek Blob formatına dönüştürülür.
    # Blob formatı, yolo modelinin istediği bir format, dönüştürmeden önce resim üzerinde bazı işlemler yapılıyor.
    # Pixel değerleri 0 ile 255 değerlerini alıyor, modelin istediği değeler 0-1 arasında olduğu normalizasyon yapılıyor.
    # Diğer bir ifadeyle her bir pixelin değeri 0-1 arasına çekiliyor.
    # size=(416,416) ile resmin boyutu 416 x 416 ya çekiliyor.
    # swapRB --> OpenCV'de görüntüler varsayılan olarak BGR (mavi-yeşil-kırmızı) formatında işlenir,
    # ancak birçok derin öğrenme modeli RGB formatını bekler.
    # Bu parametre, BGR formatını RGB'ye dönüştürmek için renk kanallarını değiştirir.
    blob = cv2.dnn.blobFromImage(image, scalefactor=1/255.0, size=(416, 416), swapRB=True, crop=False)

    # Model blob formatına dönüştürülen resim girdi olarak verilir.
    net.setInput(blob)

    # Modelin çıktıları elde edilir.
    output_layers = net.getUnconnectedOutLayersNames()
    layer_outputs = net.forward(output_layers)

    # Tespit edilen bounding box'ları eklemek için boş bir liste belirleniyor
    boxes = []
    for output in layer_outputs:
        for detection in output:
            # Yapılan tespit
            confidence = max(detection[5:])

            if confidence > 0.5:  # Confidence threshold
                box = detection[0:4] * np.array([w, h, w, h])
                (center_x, center_y, width, height) = box.astype("int")
                x = int(center_x - width / 2)
                y = int(center_y - height / 2)

                boxes.append([{'x': x, 'y': y, 'w':int(width), 'h':int(height)}])


    return boxes

def bounding_box_gonder(conn, bounding_boxes):
    boxes_str = json.dumps(bounding_boxes).encode('utf-8')
    conn.sendall(boxes_str)

while True:
    # Yeni bir bağlantı kabul ediliyor.
    conn, addr = sock.accept()
    print(f"Connected by {addr}")

    # Client tarafından gönderilen resim alınıyor
    image = resim_al(conn)

    # Bounding box'ları bul
    bounding_boxes = bounding_box_bul(image)

    # Bpunding box'ları client'a gönder
    bounding_box_gonder(conn, bounding_boxes)

    # Bağlantıyı sonlandır
    conn.close()
