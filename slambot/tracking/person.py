#!/usr/bin/env python3

import cv2, time, io, picamera
import numpy as np
from slambot.actuators.motor import Motor
from slambot.yolo.yolo import YOLOWrapper


class PersonFollower:
    def __init__(self, camera):

        self.camera = camera
        self.thresh = self.camera.im_width/12
        self.left_thresh = self.camera.im_width/2 - self.thresh
        self.right_thresh = self.camera.im_width/2 + self.thresh
        self.yolo = YOLOWrapper()

        print(f"{self.thresh} {self.left_thresh} {self.right_thresh}")

        self.PWM = Motor()
    


    def loop(self):
        try:
            # self.stream.seek(0)
            # image = cv2.imdecode(np.frombuffer(self.stream.read(), np.uint8), 1)
            # self.process_img(image)

            # self.stream.seek(0)
            # self.stream.truncate()

            self.process_img(self.camera.get_frame_matrix())
            return 1 

        except Exception as e:
            print(e)
            print ("End transmit ... " )
            return -1


    def run(self):
        while True:
        #   for _ in self.camera.capture_continuous(self.stream, 'jpeg', use_video_port = True):
            if self.loop() == -1:
                return


    def run_thread(self, exit_handler):
        while True:
        #   for _ in self.camera.capture_continuous(self.stream, 'jpeg', use_video_port = True):
            if exit_handler.is_set():
                return
            if self.loop() == -1:
                return



    @classmethod
    def get_overlay(cls, frame):
        cx, cy = self.yolo.get_person_centroid(frame)
        frame = cv2.circle(frame, (cx,cy), 20, (0,255,0), -1)
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

