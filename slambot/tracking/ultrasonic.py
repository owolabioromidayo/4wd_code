from slambot.sensors.ultrasonic import Ultrasonic
from slambot.actuators.motor import Motor
from slambot.actuators.servo import Servo

class UltrasonicTracking:
    def __init__(self, mode):
        self.motor = Motor()
        self.servo = Servo()
        self.ultrasonic = Ultrasonic()


    def run_motor(self,L,M,R):
        if (L < 30 and M < 30 and R <30) or M < 30 :
            self.motor.setMotorModel(-1450,-1450,-1450,-1450) 
            time.sleep(0.1)   
            if L < R:
                self.motor.setMotorModel(1450,1450,-1450,-1450)
            else:
                self.motor.setMotorModel(-1450,-1450,1450,1450)
        elif L < 30 and M < 30:
            self.motor.setMotorModel(1500,1500,-1500,-1500)
        elif R < 30 and M < 30:
            self.motor.setMotorModel(-1500,-1500,1500,1500)
        elif L < 20 :
            self.motor.setMotorModel(2000,2000,-500,-500)
            if L < 10 :
                self.motor.setMotorModel(1500,1500,-1000,-1000)
        elif R < 20 :
            self.motor.setMotorModel(-500,-500,2000,2000)
            if R < 10 :
                self.motor.setMotorModel(-1500,-1500,1500,1500)
        else :
            self.motor.setMotorModel(600,600,600,600)


    def loop(self):
        for i in range(30,151,60):
                self.servo.setServomotor('0',i)
                time.sleep(0.2)
                LMR[i] = self.get_distance()
                self.run_motor(*LMR)


    def run(self):
        LMR = [0,0,0]
        while True:
            self.loop(LMR)
            

    def run_thread(self, exit_handler):
        LMR = [0,0,0]
        while True:
            if exit_handler.is_set():
                self.motor.setMotorModel(0,0,0,0)
                self.servo.setServomotor('0',90)
                return
            self.loop(LMR)
            
        

