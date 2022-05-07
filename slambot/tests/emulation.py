import sys, os, time

from slambot.sensors.adc import ADC
from slambot.actuators.buzzer import Buzzer
from slambot.sensors.ultrasonic import Ultrasonic
from slambot.actuators.led import LED

from slambot.actuators.motor import Motor
from slambot.actuators.servo import Servo

class TestEmulation:
    def __init__(self):
        self.run()

    def test_adc(self):
        adc = ADC("emulate")
        assert adc.recvADC(2) == 30
        print("ADC Tests passed.")

    def test_buzzer(self):
        B = Buzzer("emulate")
        B.run('1')
        time.sleep(3)
        B.run('0')
        print("Buzzer Tests passed.")

    def test_motors(self):
        PWM = Motor("emulate")
        try:
            for fn in [PWM.goForward, PWM.goBackwards, PWM.goLeft, PWM.goRight, PWM.stop]:
                fn()
                time.sleep(1)
        except KeyboardInterrupt:
            PWM.stop()

        print("Motor Tests passed.")


    def test_servos(self):
        pwm = Servo("emulate")
        pwm.setServoPwm('0',90)
        pwm.setServoPwm('1',90)
          
        print("Servo Tests passed.")

    def test_ultrasonic(self):
        pass

    def test_led(self):
        led = LED("emulate")
        try:
            for i in range(3):
                print ("Chaser animation")
                led.colorWipe(led.strip, (255,0, 0))  # Red wipe
                led.colorWipe(led.strip, (0, 255, 0))  # Green wipe
                led.colorWipe(led.strip, (0, 0, 255))  # Blue wipe
                led.theaterChaseRainbow(led.strip)
                print ("Rainbow animation")
                led.rainbow(led.strip)
                led.rainbowCycle(led.strip)
                #all tuples except this one should be in form Color(0,0,255) from Adafruit
                led.colorWipe(led.strip, (0,0,0),10) 
        except KeyboardInterrupt:  
            led.colorWipe(led.strip, (0,0,0),10)




    def run(self):
        self.test_adc()
        self.test_buzzer()
        self.test_motors()
        self.test_servos()
        self.test_ultrasonic()
        self.test_led()

