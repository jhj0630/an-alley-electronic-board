from Bluetooth import *
from picamera import PiCamera
from tkinter import *
from PIL import ImageTk, Image
import cv2
import numpy as np
import RPi.GPIO as GPIO
import time
import datetime
import sys

root = Tk()
def dis():
    GPIO.setwarnings(Flase)
    GPIO.setmode(GPIO.BCM)
    
    trig = 2
    echo = 3
  
    GPIO.setup(trig, GPIO.OUT)
    GPIO.setup(echo, GPIO.IN)

    try:
        while True:
            GPIO.output(trig, False)
            time.sleep(0.5)

            GPIO.output(trig, True)
            time.sleep(0.00001)
            GPIO.output(trig, False)

            while GPIO.input(echo) == 0:
                pulse_start = time.time()
            while GPIO.input(echo) == 1:
                pulse_end = time.time()

            pulse_duration = pulse_end – pulse_start
            distance = pulse_duration * 17000
            distance = round(distance, 2)

            if(distance < 30):
                label1 = Label(root,text=“distance: ”+(str)distance+“cm”)
                label1.pack()
                detect()
    except KeyboardInterrupt:
        GPIO.cleanup() 

def ex():
    root.destroy()
    sys.exit()

def detect():
    cam = cv2.VideoCapture(0)
    dt = datetime.datetime.now()
    cur_time = str(dt.year) + str(dt.month) + str(dt.day) +  str(dt.hour) + str(dt.minute) + str(dt.second)
    ret, frame = cam.read()
    cv2.imwrite(cur_time+‘.jpg’, frame)

    img1 = ImageTk.PhotoImage(Image.open(cur_time+‘.jpg’))
    label2 = Label(root, image = img1)
    label2.pack()

    YOLO_net =cv2.dnn.readNet(“yolov3.weights”
    ,“yolov3.cfg”)
    classes = []
    with open(“coco.names”, “r”) as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = YOLO.getLayerNames()
    output_layers = [layer_names[i-1] for i 
    in YOLO_net.getUnconnectedOutLayers()]


    colors = np.random.uniform(0, 255, size=(len(classes), 3))

    img = cv2.imread(name)   
    img = cv2.resize(img, None, fx = 0.4, fy = 0.4)
    height, width, channels = img.shape
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416)
    , (0, 0, 0) ,True, crop = False)
    YOLO_net.setInput(blob)
    outs = YOLO_net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            scores = detection[5: ]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0]*width)
                center_y = int(detection[1]*height)
                dw = int(detection[2]*width)
                dh = int(detection[3]*height)

 
                x = int(center_x – dw / 2)
                y = int
                boxes.append([x,  y, dw, dh])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.45
    , 0.4)

for i in range(len(boxes)):
        if i in indexes:
            x, y, dw, dh = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[i]
            cv2.rectangle(image, (x, y), (x+dw, y+dh), color, 2)
            cv2.putText(img, label, (x, y+30), cv2.FONT_ITALIC,             
            3, color, 3)
    cv2.imwrite(cur_time+‘yolo.jpg’, img)
    label3 = Label(root, image = cur_time+‘yolo.jpg’)
    label3.pack()
    
    if label == “car”:
        msg = “1”
        label4 = Label(root, text = “result: car”)
    elif label == “person”:
        msg = “2”
        label4 = Label(root, text = “result: person”)
    else:
        msg = “0”
        label4 = Label(root, text = “result: nothing”)
    label4.pack()
    exitButton = Button(root, text = “exit”, command = ex)
    exitButton.pack()
    lightOn(msg)   
 
def lightOn(msg):
    client_socket = BluetoothSocket(RFCOMM)
    client_socket.connect((“98:DA:60:05:CD:74”, 1))

    while True:
        client_socket.send(msg)
        root.mainloop()
    client_socket.close()

dis()
