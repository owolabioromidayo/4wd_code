import time
from slambot.sensors.PCA9685 import PCA9685

class Servo:
    def __init__(self, mode=""):
        self.mode = mode
        if self.mode != "emulate":
            self.PwmServo = PCA9685(0x40, debug=True)
        else:
            self.PwmServo = PCA9685(0x40, True, "emulate")

        self.PwmServo.setPWMFreq(50)
        self.PwmServo.setServoPulse(8,1500)
        self.PwmServo.setServoPulse(9,1500)

        self.horiz_ang = 90
        self.vert_ang = 90


    def setServoPwm(self,channel,angle,error=10):
        print(f"Setting channel {channel} to angle {angle}.")

        angle=int(angle)
        if channel=='0':
            self.PwmServo.setServoPulse(8,2500-int((angle+error)/0.09))
        elif channel in '1234567':
            self.PwmServo.setServoPulse(int(channel)+8, 500+int((angle+error)/0.09))
            self.PwmServo.setServoPulse(9,500+int((angle+error)/0.09))
        

    def home(self):
        print("Homing servos")

        self.horiz_ang = 90
        self.vert_ang = 90
        self.setServoPwm('0',self.horiz_ang)
        self.setServoPwm('1',self.vert_ang)

    def nudgeHoriz(self, val):
        print(f"Moving servo horizontally by {val} degrees.")

        if  50 <= self.horiz_ang + val <= 110:    
            self.horiz_ang += val
            self.setServoPwm('0', self.horiz_ang)
        else:
            print("Out of steering range")
        

    def nudgeVert(self, val):
        print(f"Moving servo vertically by {val} degrees.")

        if 80 <= self.vert_ang + val <= 150:
            self.vert_ang += val
            self.setServoPwm('1', self.vert_ang)
        else:
            print("Out of steering range")
    

    

    
       



    
