import cv2
 
class YOLOWrapper: 
    def __init__(self):
        net = cv2.dnn.readNetFromDarknet('yolov4.cfg', 'yolov4.weights')
        
        self.model = cv2.dnn_DetectionModel(net)
        self.model.setInputParams(scale=1 / 255, size=(416, 416), swapRB=True)

        with open('coco.names', 'r') as f:
            self.classes = f.read().splitlines()

    def get_labelled_image(self, img):
        classIds, scores, boxes = self.model.detect(img, confThreshold=0.6, nmsThreshold=0.4)
        
        for (classId, score, box) in zip(classIds, scores, boxes):
            cv2.rectangle(img, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]),
                        color=(0, 255, 0), thickness=2)
        
            text = '%s: %.2f' % (self.classes[classId[0]], score)
            cv2.putText(img, text, (box[0], box[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        color=(0, 255, 0), thickness=2)
                    
        return img 
    

    def get_person_centroid(self, img):
        classIds, scores, boxes = self.model.detect(img, confThreshold=0.6, nmsThreshold=0.4)

        for (classId, score, box) in zip(classIds, scores, boxes):
            if self.classes[classId] == "person": #this works for only the first person it finds
                print(box)
                cx = box[0] + box[2] / 2
                cy = box[1] + box[3] / 2
                return cx,cy 

        return None, None    #No person found


a = YOLOWrapper()
im = cv2.imread("./test.jpg")
im2 = cv2.imread("./test2.png")

print(a.get_person_centroid(im))
print(a.get_person_centroid(im2))

 