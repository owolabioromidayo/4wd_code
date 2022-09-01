#Modified by smartbuilds.io
#Date: 27.09.20
#Desc: This scrtipt script..

import cv2
from imutils.video.pivideostream import PiVideoStream
import imutils
import time
import numpy as np
from slambot.tracking.line import Follower
from slambot.tracking.person import PersonFollower

class VideoCamera(object):
    def __init__(self, flip = False):
        self.im_width =600
        self.im_height = 400
        self.vs = PiVideoStream(resolution=(self.im_width,self.im_height), framerate=30).start()
        self.flip = flip
        time.sleep(2.0)
        self.mode = "default"

    def __del__(self):
        self.vs.stop()

    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame

    def get_frame(self):
        frame = self.flip_if_needed(self.vs.read())

        if self.mode == "line_following": 
            frame = Follower.get_overlay(frame)

        elif self.mode == "person_tracking": 
            frame = PersonFollower.get_overlay(frame)

        else:
            pass #default, no overlays
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    def get_frame_matrix(self):
        return self.flip_if_needed(self.vs.read())

