import tkinter as tk
from PIL import Image, ImageTk
import time, socket, json, cv2, os

root = tk.Tk()
root.title("Mert Musluoğlu 171")

HOST = '127.0.0.1'
PORT = 12345

desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
output_dir = os.path.join(desktop_path, 'improved_images')

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

NAMES_PATH = 'ai/coco.names'
with open(NAMES_PATH, 'r') as f:
    classes = [line.strip() for line in f.readlines()]

def draw_bbox(image, bbox, class_ids):
    for i, box in enumerate(bbox):
        x, y, w, h = box[:4]
        class_id = class_ids[i]
        confidence = box[5]
        label = f"{classes[class_id]}: {confidence:.2f}"

        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    return image

def show_image(image_path, box_info, image_index):
    bbox = [box[:6] for box in box_info]
    class_ids = [box[4] for box in box_info]

    img = cv2.imread(image_path)

    img_with_boxes = draw_bbox(img, bbox, class_ids)

    img_rgb = cv2.cvtColor(img_with_boxes, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_pil = img_pil.resize((500, 500))
    img_tk = ImageTk.PhotoImage(img_pil)

    image_label = tk.Label(root, image=img_tk)
    image_label.image = img_tk
    image_label.pack()

    box_text = "Bounding Box:\n"
    for box in box_info:
        x, y, w, h = box[:4]
        class_id = box[4]
        confidence = box[5]
        box_text += f"Sınıf: {classes[class_id]}, Koordinatlar: ({x}, {y}, {w}, {h}), Confidence: {confidence:.2f}\n"

    text_label = tk.Label(root, text=box_text)
    text_label.pack()

    root.update()

    output_path = os.path.join(output_dir, f'improved_image{image_index + 1}.jpg')
    cv2.imwrite(output_path, img_with_boxes)
    print(f"Görüntü kaydedildi: {output_path}")

    time.sleep(5)

    image_label.pack_forget()
    text_label.pack_forget()

def receive_data():
    image_paths = [
        'images/image1.jpg',
        'images/image2.jpg',
        'images/image3.jpg',
        'images/image4.jpg',
        'images/image5.jpg',
        'images/image6.jpg'
    ]
    
    for idx, image_path in enumerate(image_paths):
        data_size = client_socket.recv(10).decode('utf-8').strip()
        if not data_size:
            break

        data_size = int(data_size)
        data = client_socket.recv(data_size).decode('utf-8')
        boxes = json.loads(data)

        show_image(image_path, boxes, idx)

receive_data()

root.mainloop()

client_socket.close()
