import numpy as np
import cv2 as cv

net = cv.dnn.readNet("ai/yolov4-tiny.weights", "ai/yolov4-tiny.cfg")

with open("ai/coco.names", "r") as file:
    classes = file.read().strip().split("\n")

images = [cv.imread(f"images/image{i + 1}.jpg") for i in range(6)]

width1, height1 = images[0].shape[1], images[0].shape[0]
width2, height2 = images[1].shape[1], images[1].shape[0]
width3, height3 = images[2].shape[1], images[2].shape[0]
width4, height4 = images[3].shape[1], images[3].shape[0]
width5, height5 = images[4].shape[1], images[4].shape[0]
width6, height6 = images[5].shape[1], images[5].shape[0]

widths = [width1, width2, width3, width4, width5, width6]
heights = [height1, height2, height3, height4, height5, height6]

class AI():
    def __init__(self, index):
        global boxes
        global confidences
        global class_ids
        global blob
        global outputs
        global detected_objects

        blob = cv.dnn.blobFromImage(images[index], 1/255.0, (416, 416), swapRB=True, crop=False)

        net.setInput(blob)

        layer_names = net.getLayerNames()

        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

        outputs = net.forward(output_layers)

        boxes = []
        confidences = []
        class_ids = []
        detected_objects = []

        self.detect(index)

    def detect(self, index):
        for output in outputs:
            for detection in output:
                scores = detection[5:]

                class_id = np.argmax(scores)

                confidence = scores[class_id]

                if confidence > 0.5:
                    box = detection[0:4] * np.array([widths[index], heights[index], widths[index], heights[index]])

                    (centerX, centerY, boxWidth, boxHeight) = box.astype("int")

                    x = int(centerX - (boxWidth / 2))
                    y = int(centerY - (boxHeight / 2))

                    boxes.append([x, y, int(boxWidth), int(boxHeight)])
                    class_ids.append(class_id)
                    confidences.append(float(confidence))

        self.draw(index)

    def draw(self, index):
        indices = cv.dnn.NMSBoxes(boxes, confidences, score_threshold=0.5, nms_threshold=0.4)
        
        if len(indices) > 0:
            for i in indices.flatten():
                x, y, w, h = boxes[i]

                detected_objects.append({
                    'class_id' : class_ids[i],
                    'confidence' : confidences[i],
                    'class_name' : classes[class_ids[i]],
                    'box' : [x, y, w, h]
                })
        
        for object in detected_objects:
            x, y, w, h = object['box']

            text = f"{object["class_name"]} : {object['confidence']:.2f}"

            cv.rectangle(images[index], (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv.putText(images[index], text, (x, y - 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            file = open("data.txt", "a")
            file.write(f"Class: {object['class_name']}, Confidence: {object['confidence']:.2f}, Box: [{x}, y={y}, w={w}, h={h}]\n")

    def save(self, images):
        for i in range(6):
            cv.imwrite(f"images_new/image_new{i + 1}.jpg", images[i])
        
if __name__ == "__main__":
    names = ["first", "second", "third", "fourth", "fifth", "sixth"]

    for i in range(6):
        ai = AI(i)
        cv.imshow(names[i], images[i])
    
    ai.save(images)
    
    cv.waitKey(0)
    cv.destroyAllWindows()