import torch
import cv2
import pandas as pd
import requests
from PIL import Image
import cv2
from ultralytics import YOLO

car_deque = {}

def yolov8_strong(partition_xyxy, frame):
    
    # Load the YOLOv8 model
    model = YOLO('yolov8n.pt')

    print(partition_xyxy[0][0], partition_xyxy[0][1], partition_xyxy[1][0], partition_xyxy[1][1])
    x1_new = partition_xyxy[0][0]
    y1_new = partition_xyxy[0][1]
    x2_new = partition_xyxy[1][0]
    y2_new = partition_xyxy[1][1]

    partition_frame = frame[y1_new:y2_new, x1_new:x2_new]
    results = model(partition_frame)

    # Visualize the results on the frame
    annotated_frame = results[0].plot()
    for r in results:
        if r.probs==None:
            print("Number of Cars:", str(0))
        else:
            print("Number of Cars:", len(r.probs))
    #print("Result probs: ", results[0])

    # Display the annotated frame
    cv2.imshow("YOLOv8 Inference", annotated_frame)

def yolov5_light(video):
    partition_xyxy = []
    model = torch.hub.load('yolov5', 'yolov5n', source='local')

    cap = cv2.VideoCapture(video)
    count_send = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        result = model(frame)
        df = result.pandas().xyxy[0]
        #print("box df: ",df.iloc[0].loc['name'])
        for ind in df.index:
            x1,y1 = int(df['xmin'][ind]) , int(df['ymin'][ind])
            x2,y2 = int(df['xmax'][ind]), int(df['ymax'][ind])

            label = df['name'][ind]
            conf = df['confidence'][ind]
            text = label +'' + str(conf.round(2))
            cv2.rectangle(frame,(x1,y1),(x2,y2),(255,255,0),2)                                    
            cv2.rectangle(frame,(x1-200,y1-500),(x1+150,y1-100),(0,255,255),2)
            #cv2.putText(frame,text,(x1,y1-5),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,0),2)

        if count_send==5:
            #print(partition_xyxy)
            partition_xyxy.append((x1-200,y1-500))  #select the partition according to ego car
            partition_xyxy.append((x1+150,y1-100))
            yolov8_strong(partition_xyxy, frame) 

        cv2.imshow('video',frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        count_send+=1
    cap.release()   
    cv2.destroyAllWindows()
    #return 

if __name__ == '__main__':
    video = 'video_file1.mp4'
    yolov5_light(video)
    #yolov8_strong(partition_xyxy, frame)
    



