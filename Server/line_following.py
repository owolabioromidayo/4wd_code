#!/usr/bin/env python3
import cv2, picamera, time, io
import numpy as np
from Motor import *


class Follower:
    def __init__(self):
        #cv2.namedWindow("rgb", 1)
        #cv2.namedWindow("hsv", 1)
        #cv2.namedWindow("masked", 1)

        self.im_width = 1280 
        self.im_height = 720
        self.thresh = self.im_width/12
        self.left_thresh = self.im_width/2 - self.thresh
        self.right_thresh = self.im_width/2 + self.thresh

        print(f"{self.thresh} {self.left_thresh} {self.right_thresh}")
        self.camera = picamera.PiCamera(resolution=(self.im_width,self.im_height), framerate = 60 )
                
        time.sleep(2)                      
        self.start = time.time()
        self.stream = io.BytesIO()
        print("Camera: ACTIVE ... ")

        self.PWM = Motor()
        print("MOtor: CONNECTED...")

    
        self.run()
            
    def run(self):
          for _ in self.camera.capture_continuous(self.stream, 'jpeg', use_video_port = True):
            try:
                self.stream.seek(0)
                image = cv2.imdecode(np.frombuffer(self.stream.read(), np.uint8), 1)
                self.process_img(image)

                self.stream.seek(0)
                self.stream.truncate()

            except Exception as e:
                print(e)
                print ("End transmit ... " )
                break

    def run_thread(self, exit_handler):

          for _ in self.camera.capture_continuous(self.stream, 'jpeg', use_video_port = True):
            if exit_handler.is_set():
                return
            try:
                self.stream.seek(0)
                image = cv2.imdecode(np.frombuffer(self.stream.read(), np.uint8), 1)
                self.process_img(image)

                self.stream.seek(0)
                self.stream.truncate()

            except Exception as e:
                print(e)
                print ("End transmit ... " )
                break

        # while True:
        #     self.camera.capture('/home/pi/curr.jpg')

        #     rgb, hsv, masked  = self.process_img(data)
        #     cv2.imshow("rgb", rgb)
        #     cv2.imshow("hsv", hsv)
        #     cv2.imshow("masked", masked)
        #     cv2.waitKey(3)

        #     time.sleep(0.5)

    def process_img(self, image):
        #color filtering
        rgb = image
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        lower_yellow = np.array([60, 0, 0])
        upper_yellow = np.array([120, 255, 255])
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        #masked = cv2.bitwise_and(image, image, mask=mask)


        #computing moments
        h,w,d = image.shape
        search_top = int(3*h/4)
        search_bot = search_top + 20
        mask[0:search_top, 0:w] = 0
        mask[search_bot:h, 0:w] = 0

        M = cv2.moments(mask)
        if M['m00'] > 0 :
            cx = int (M['m10']/ M['m00'])
            cy = int (M['m01']/ M['m00'])
            cv2.circle(rgb, (cx,cy), 20, (0,255,255), -1)


            #follow the dot/ publish to cmd_vel
            motor_duties = [-1000,-1000,-1000,-1000]
            
        
            print(f"CX: {cx}")

            if self.left_thresh<cx<self.right_thresh:
                print('GOING STRAIGHT')

            elif cx <= self.left_thresh:
                print('GOING LEFT')
                #motor_duties = list(map(lambda x: min(int(x*scale), 1) ,[-500, -500, 2000, 2000]))
                motor_duties = [-500, -500, -2000,-2000 ]

            else:
                print('GOING RIGHT')
                #motor_duties = list(map(lambda x: min(int(x*scale), 1) ,[2000, 2000, -500, -500]))
                motor_duties = [-2000,-2000,-500,-500]

            self.PWM.setMotorModel(*motor_duties)
            print(motor_duties)

        #cv2.imshow("rgb", rgb)
        #cv2.imshow("hsv", hsv)
        #cv2.imshow("masked", masked)
        cv2.waitKey(3)

        #time.sleep(0.5)

        return 


if __name__ == "__main__":
    follower = Follower()
