import time
from slambot.actuators.motor import Motor
import RPi.GPIO as GPIO

class Line_Tracking:
    def __init__(self):
        self.IR01 = 14
        self.IR02 = 15
        self.IR03 = 23
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.IR01,GPIO.IN)
        GPIO.setup(self.IR02,GPIO.IN)
        GPIO.setup(self.IR03,GPIO.IN)

    def loop(self):
        self.LMR=0x00
        if GPIO.input(self.IR01)==True:
            self.LMR=(self.LMR | 4)
        if GPIO.input(self.IR02)==True:
            self.LMR=(self.LMR | 2)
        if GPIO.input(self.IR03)==True:
            self.LMR=(self.LMR | 1)

        dispatch = {
            1: (2500,2500,-1500,-1500),
            2: (800,800,800,800),
            3: (4000,4000,-2000,-2000),
            4: (-1500,-1500,2500,2500),
            6: (-2000,-2000,4000,4000),
            7: (0,0,0,0)
        }
        PWM.setMotorModel(*dispatch[self.LMR])


    def run(self):
        while True:
            self.loop()
           

    def run_thread(self, exit_handler):        
        while True:
            if exit_handler.is_set():
                return
            self.loop()
            
