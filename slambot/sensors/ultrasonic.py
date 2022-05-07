import time
from slambot.actuators.motor import Motor
from slambot.sensors.PCA9685 import PCA9685
from slambot.actuators.servo import Servo

try: 
    import RPi.GPIO as GPIO
except: 
    print("Failed to import RPi.GPIO . Could be runnning in emulation mode.")



class Ultrasonic:
    def __init__(self, mode=""):
        self.mode = mode
        if self.mode != "emulate":
            GPIO.setwarnings(False)
            self.trigger_pin = 27
            self.echo_pin = 22
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.trigger_pin,GPIO.OUT)
            GPIO.setup(self.echo_pin,GPIO.IN)
        else:
            print(f"{self.__class__.__name__} running in emulation mode.")  


    def send_trigger_pulse(self):
        print("Sending trigger pulse on Ultrasonic")
        if self.mode != "emulate":
            GPIO.output(self.trigger_pin,True)
            time.sleep(0.00015)
            GPIO.output(self.trigger_pin,False)
                 

    def wait_for_echo(self,value,timeout):
        print("Waiting for echo Ultrasonic")
        if self.mode != "emulate":
            while GPIO.input(self.echo_pin) != value and timeout>0:
                timeout -= 1
     

    def get_distance(self):
        print("Getting distance from Ultrasonic.")

        if self.mode != "emulate":
            #seems to sort then take median distance -> requires further investigation
            distance_cm=[0,0,0,0,0]
            for i in range(3):
                self.send_trigger_pulse()
                self.wait_for_echo(True,10000)
                start = time.time()
                self.wait_for_echo(False,10000)
                finish = time.time()
                pulse_len = finish-start
                distance_cm[i] = pulse_len/0.000058
            distance_cm=sorted(distance_cm)
            return int(distance_cm[2])

        else:
            return 30




