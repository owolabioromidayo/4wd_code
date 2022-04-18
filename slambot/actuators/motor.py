import time
from slambot.sensors.PCA9685 import PCA9685
class Motor:
    def __init__(self, mode=""):
        self.mode = mode
        if self.mode == "emulate":
            print(f"{self.__class__.__name__} running in emulation mode.") 
            self.pwm = PCA9685(0x40, debug=True, mode="emulate")
        else:
            self.pwm = PCA9685(0x40, debug=True)

        self.pwm.setPWMFreq(50)

    def duty_range(self,duty1,duty2,duty3,duty4):
        duty1 = min(max(-4095, duty1), 4095)
        duty2 = min(max(-4095, duty2), 4095)
        duty3 = min(max(-4095, duty3), 4095)
        duty4 = min(max(-4095, duty4), 4095)

        return duty1,duty2,duty3,duty4
        
    def left_Upper_Wheel(self,duty):
        if duty>0:
            self.pwm.setMotorPwm(0,0)
            self.pwm.setMotorPwm(1,duty)
        elif duty<0:
            self.pwm.setMotorPwm(1,0)
            self.pwm.setMotorPwm(0,abs(duty))
        else:
            self.pwm.setMotorPwm(0,4095)
            self.pwm.setMotorPwm(1,4095)

    def left_Lower_Wheel(self,duty):
        if duty>0:
            self.pwm.setMotorPwm(3,0)
            self.pwm.setMotorPwm(2,duty)
        elif duty<0:
            self.pwm.setMotorPwm(2,0)
            self.pwm.setMotorPwm(3,abs(duty))
        else:
            self.pwm.setMotorPwm(2,4095)
            self.pwm.setMotorPwm(3,4095)
            
    def right_Upper_Wheel(self,duty):
        if duty>0:
            self.pwm.setMotorPwm(6,0)
            self.pwm.setMotorPwm(7,duty)
        elif duty<0:
            self.pwm.setMotorPwm(7,0)
            self.pwm.setMotorPwm(6,abs(duty))
        else:
            self.pwm.setMotorPwm(6,4095)
            self.pwm.setMotorPwm(7,4095)

    def right_Lower_Wheel(self,duty):
        if duty>0:
            self.pwm.setMotorPwm(4,0)
            self.pwm.setMotorPwm(5,duty)
        elif duty<0:
            self.pwm.setMotorPwm(5,0)
            self.pwm.setMotorPwm(4,abs(duty))
        else:
            self.pwm.setMotorPwm(4,4095)
            self.pwm.setMotorPwm(5,4095)
            
 
    def setMotorModel(self,duty1,duty2,duty3,duty4):
        duty1,duty2,duty3,duty4=self.duty_range(duty1,duty2,duty3,duty4)
        self.left_Upper_Wheel(duty1)
        self.left_Lower_Wheel(duty2)
        self.right_Upper_Wheel(duty3)
        self.right_Lower_Wheel(duty4)


    def goForward(self):
        print("Going forward.")
        self.setMotorModel(600,600,600,600)      

    def goBackwards(self):
        print("Going backwards.")
        self.setMotorModel(-600,-600,-600,-600)      
            
    def goLeft(self):
        print("Going left.")
        self.setMotorModel(-1200,-1200,1400,1400)      
            
    def goRight(self):
        print("Going right.")
        self.setMotorModel(1400,1400,-1200,-1200)  

    def stop(self):
        print("Stopping wheel motors.")
        self.setMotorModel(0,0,0,0)    


