import time
from slambot.actuators.motor import Motor
from slambot.sensors.adc import ADC

class Light:
    def __init__(self):
        self.adc=ADC()
        self.PWM=Motor()
        self.PWM.setMotorModel(0,0,0,0)

    def run(self):
        while True:
                self.loop()

    def run_thread(self, exit_handler):
        while True:
            if exit_handler.is_set():
                return
            self.loop()

    def loop(self):
        L = self.adc.recvADC(0)
        R = self.adc.recvADC(1)
        if L < 2.99 and R < 2.99 :
            self.PWM.goForwards()

        elif abs(L-R)<0.15:
            self.PWM.stop()
            
        elif L > 3 or R > 3:
            if L > R :
                self.PWM.goLeft()
                
            elif R > L :
                self.PWM.goRight()

