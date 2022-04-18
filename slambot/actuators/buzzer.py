try: import RPi.GPIO as GPIO
except: print("Failed to import Rpi.GPIO. Could be runnning in emulation mode")


class Buzzer:
    def __init__(self, mode=""):
        self.mode = mode
        if self.mode != "emulate":
            self.buzzer_pin = 17
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.buzzer_pin,GPIO.OUT)
        else:
            print(f"{self.__class__.__name__} running in emulation mode.") 
 
    def run(self,command):
        if self.mode != "emulate":
            if command !="0":
                GPIO.output(self.buzzer_pin,True)
            else:
                GPIO.output(self.buzzer_pin,False)
        else:
            if command !="0":
                print("Buzzer on.")
            else:
                print("Buzzer off.")

            
        





