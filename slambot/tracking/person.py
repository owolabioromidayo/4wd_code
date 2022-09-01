#!/usr/bin/env python3

import cv2, time, io, picamera
import numpy as np
from slambot.actuators.motor import Motor
from slambot.yolo.yolo import YOLOWrapper


class PersonFollower:
    def __init__(self):

        self.im_width = 1280 
        self.im_height = 720
        self.thresh = self.im_width/12
        self.left_thresh = self.im_width/2 - self.thresh
        self.right_thresh = self.im_width/2 + self.thresh
        self.yolo = YOLOWrapper()

        print(f"{self.thresh} {self.left_thresh} {self.right_thresh}")
        self.camera = picamera.PiCamera(resolution=(self.im_width,self.im_height), framerate = 60 )
                
        time.sleep(2)                      
        self.start = time.time()
        self.stream = io.BytesIO()
        print("Camera: ACTIVE ... ")

        self.PWM = Motor()
        print("MOtor: CONNECTED...")
    
        self.run()


    def loop(self):
        try:
            self.stream.seek(0)
            image = cv2.imdecode(np.frombuffer(self.stream.read(), np.uint8), 1)
            self.process_img(image)

            self.stream.seek(0)
            self.stream.truncate()

        except Exception as e:
            print(e)
            print ("End transmit ... " )


    def run(self):
          for _ in self.camera.capture_continuous(self.stream, 'jpeg', use_video_port = True):
            self.loop()


    def run_thread(self, exit_handler):
          for _ in self.camera.capture_continuous(self.stream, 'jpeg', use_video_port = True):
            if exit_handler.is_set():
                return
            self.loop()



    @classmethod
    def get_overlay(cls, frame):
        cx, cy = self.yolo.get_person_centroid(frame)
        cv2.circle(frame, (cx,cy), 20, (255,0,255), -1)
        return frame

    def process_img(self, image):
        cx, cy = self.yolo.get_person_centroid(image)
        if (cx, cy) == (None, None):
            self.PWM.stop()
            return

        if(cy > self.im_height / 2): #if yp is too high, the person is right in front of you
            self.PWM.stop()
        elif(cx < ((self.im_width /2) - 50 )): #go left
            print('GOING LEFT')
            self.PWM.goLeft()
        elif(cx > ((self.im_width /2) + 50 )): #go right 
            print('GOING RIGHT')
            self.PWM.goRight()
        else:
            self.PWM.goForward()

        # cv2.waitKey(3)
        return 

