#!/usr/bin/python

import time
import math
try: import smbus
except: print("Failed to import smbus. Could be runnning in emulation mode.")



# ============================================================================
# Raspi PCA9685 16-Channel PWM Servo Driver
# ============================================================================

class PCA9685:

  # Registers/etc.
	__SUBADR1            = 0x02
	__SUBADR2            = 0x03
	__SUBADR3            = 0x04
	__MODE1              = 0x00
	__PRESCALE           = 0xFE
	__LED0_ON_L          = 0x06
	__LED0_ON_H          = 0x07
	__LED0_OFF_L         = 0x08
	__LED0_OFF_H         = 0x09
	__ALLLED_ON_L        = 0xFA
	__ALLLED_ON_H        = 0xFB
	__ALLLED_OFF_L       = 0xFC
	__ALLLED_OFF_H       = 0xFD

	def __init__(self, address=0x40, debug=False, mode=""):
		self.mode = mode
		if (self.mode == "emulate"):
			print(f"{self.__class__.__name__} running in emulation mode.")  

		if self.mode != "emulate":
			self.bus = smbus.SMBus(1)
			self.address = address
			self.debug = debug
			self.write(self.__MODE1, 0x00)
	

	def write(self, reg, value):
		"Writes an 8-bit value to the specified register/address"

		print(f"Writing {value} to register {reg}")

		if self.mode != "emulate":
			self.bus.write_byte_data(self.address, reg, value)
		
	  
	def read(self, reg):
		"Read an unsigned byte from the I2C device"

		print("Reading from reg {reg}.")

		if self.mode != "emulate":
			result = self.bus.read_byte_data(self.address, reg)
			return result

	
	def setPWMFreq(self, freq):
		"Sets the PWM frequency"

		print(f"Setting PWM frequency to {freq}")

		if self.mode != "emulate":
			prescaleval = 25000000.0    # 25MHz
			prescaleval /= 4096.0       # 12-bit
			prescaleval /= float(freq)
			prescaleval -= 1.0
			prescale = math.floor(prescaleval + 0.5)

			oldmode = self.read(self.__MODE1)
			newmode = (oldmode & 0x7F) | 0x10        # sleep
			self.write(self.__MODE1, newmode)        # go to sleep
			self.write(self.__PRESCALE, int(math.floor(prescale)))
			self.write(self.__MODE1, oldmode)
			time.sleep(0.005)
			self.write(self.__MODE1, oldmode | 0x80)
	

	def setPWM(self, channel, on, off):
		"Sets a single PWM channel"

		print(f"Setting PWM channel {channel}, on: {on}, off{off}")

		if self.mode != "emulate":
			self.write(self.__LED0_ON_L+4*channel, on & 0xFF)
			self.write(self.__LED0_ON_H+4*channel, on >> 8)
			self.write(self.__LED0_OFF_L+4*channel, off & 0xFF)
			self.write(self.__LED0_OFF_H+4*channel, off >> 8)
	

	def setMotorPwm(self,channel,duty):
		print(f"Setting channel {channel} to duty {duty}.")

		if self.mode != "emulate":
			self.setPWM(channel,0,duty)


	def setServoPulse(self, channel, pulse):
		"Sets the Servo Pulse,The PWM frequency must be 50HZ"

		print(f"Setting servo pulse in channel {channel} to  pulse {pulse}")

		if self.mode !="emulate":
			pulse = pulse*4096/20000 #PWM frequency is 50HZ,the period is 20000us
			self.setPWM(channel, 0, int(pulse))

	
	  
