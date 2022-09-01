#!/usr/bin/env python3

import cv2, time, io, picamera
import numpy as np
from slambot.actuators.motor import Motor
from slambot.yolo.yolo import YOLOWrapper


class PersonFollower:
    def __init__(self, camera = None):

        self.camera = camera
        if self.camera:
            self.thresh = self.camera.im_width/12
            self.left_thresh = self.camera.im_width/2 - self.thresh
            self.right_thresh = self.camera.im_width/2 + self.thresh
            print(f"{self.thresh} {self.left_thresh} {self.right_thresh}")
            self.PWM = Motor()

        self.yolo = YOLOWrapper()

    


    def loop(self):
        if not self.camera:
            return
        try:
            self.process_img(self.camera.get_frame_matrix())
            return 1 

        except Exception as e:
            print(e)
            print ("End transmit ... " )
            return -1


    def run(self):
        if not self.camera:
            return
        while True:
            if self.loop() == -1:
                return


    def run_thread(self, exit_handler):
        if not self.camera:
            return
        while True:
            if exit_handler.is_set():
                return
            if self.loop() == -1:
                return



    def get_overlay(self, frame):
        
        #its too slow, just return the frame
        return frame
        try:
            cx, cy = self.yolo.get_person_centroid(frame)
            frame = cv2.circle(frame, (cx,cy), 20, (0,255,0), -1)
        except:
            pass
        return frame

    def process_img(self, image):
        if not self.camera:
            return
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

        return 

