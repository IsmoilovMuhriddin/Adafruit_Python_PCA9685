# Copyright (c) 2016 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
from __future__ import division
import logging
import time
import math
import  wiringpi as wp

# Registers/etc:
PCA9685_ADDRESS    = 0x40
MODE1              = 0x00
MODE2              = 0x01
SUBADR1            = 0x02
SUBADR2            = 0x03
SUBADR3            = 0x04
PRESCALE           = 0xFE
LED0_ON_L          = 0x06
LED0_ON_H          = 0x07
LED0_OFF_L         = 0x08
LED0_OFF_H         = 0x09
ALL_LED_ON_L       = 0xFA
ALL_LED_ON_H       = 0xFB
ALL_LED_OFF_L      = 0xFC
ALL_LED_OFF_H      = 0xFD

# Bits:
RESTART            = 0x80
SLEEP              = 0x10
ALLCALL            = 0x01
INVRT              = 0x10
OUTDRV             = 0x04

LOW_PIN = 0
HIGH_PIN=1

MAX_SPEED   =   	250
NOR_SPEED   =   	120
MIN_SPEED   =   	0

MOTOR_START_DELAY	=10 

logger = logging.getLogger(__name__)


def software_reset(i2c=None, **kwargs):
    """Sends a software reset (SWRST) command to all servo drivers on the bus."""
    # Setup I2C interface for device 0x00 to talk to all of them.
    if i2c is None:
        import Adafruit_GPIO.I2C as I2C
        i2c = I2C

    self.fd= wp.wiringPiI2CSetup(0x60);    
    wp.wiringPiI2CWriteReg8(fd,0x06)# SWRST


class PCA9685(object):
    """PCA9685 PWM LED/servo controller."""

    def __init__(self, address=PCA9685_ADDRESS, i2c=None, **kwargs):
        """Initialize the PCA9685."""
        # private variables of class
        #self.fd
        self.nSpeed = NOR_SPEED
        self.enAPin = 0
        self.en1Pin = 1
        self.en2Pin = 2
        self.enBPin = 5
        self.en3Pin = 3
        self.en4Pin = 4
        self.BuzzPin= 8
        self.fd= wp.wiringPiI2CSetup(0x60);
        self.init_start()
    
    def init_start(self):
        # Setup I2C interface for the device.
        
        self.set_all_pwm(0, 0)
        wp.wiringPiI2CWriteReg8(fd, MODE1, OUTDRV);
        wp.wiringPiI2CWriteReg8(fd, MODE1, ALLCALL);
        time.sleep(0.005)  # wait for oscillator
        mode1 = wp.wiringPiI2CReadReg8(fd, MODE1);
        mode1 = mode1 & ~SLEEP;  # wake up (reset sleep)
        wp.wiringPiI2CWriteReg8(fd, MODE1, mode1);
        time.sleep(0.005)  # wait for oscillator
        set_pwm_freq(1000)

    def set_pwm_freq(self, freq_hz):
        """Set the PWM frequency to the provided value in hertz."""
        prescaleval = 25000000.0    # 25MHz
        prescaleval /= 4096.0       # 12-bit
        prescaleval /= float(freq_hz)
        prescaleval -= 0.5
        logger.debug('Setting PWM frequency to {0} Hz'.format(freq_hz))
        logger.debug('Estimated pre-scale: {0}'.format(prescaleval))
        prescale = int(math.floor(prescaleval + 0.5))
        logger.debug('Final pre-scale: {0}'.format(prescale))
        oldmode = wp.wiringPiI2CReadReg8(fd, MODE1);
        newmode = (oldmode & 0x7F) | 0x10;           
        wp.wiringPiI2CWriteReg8(fd,MODE1, newmode)  # go to sleep
        wp.wiringPiI2CWriteReg8(fd,PRESCALE, prescale)
        wp.wiringPiI2CWriteReg8(fd,MODE1, oldmode)
        time.sleep(0.005)
        wp.wiringPiI2CWriteReg8(fd,MODE1, oldmode | 0x80)

    def set_pwm(self, channel, on, off):
        """Sets a single PWM channel."""
        wp.wiringPiI2CWriteReg8(fd,LED0_ON_L+4*channel, on & 0xFF)
        wp.wiringPiI2CWriteReg8(fd,LED0_ON_H+4*channel, on >> 8)
        wp.wiringPiI2CWriteReg8(fd,LED0_OFF_L+4*channel, off & 0xFF)
        wp.wiringPiI2CWriteReg8(fd,LED0_OFF_H+4*channel, off >> 8)

    def set_all_pwm(self, on, off):
        """Sets all PWM channels."""
        wp.wiringPiI2CWriteReg8(fd,ALL_LED_ON_L, on & 0xFF)
        wp.wiringPiI2CWriteReg8(fd,ALL_LED_ON_H, on >> 8)
        wp.wiringPiI2CWriteReg8(fd,ALL_LED_OFF_L, off & 0xFF)
        wp.wiringPiI2CWriteReg8(fd,ALL_LED_OFF_H, off >> 8)
    def set_pin(self, pin,value):
        if value==0:
            set_pwm(pin,0,4096)
        if value==1:
            set_pwm(pin,4096,0)
    
    def go_forward(self):
        set_pin(en1Pin,LOW_PIN)
        set_pin(en2Pin,HIGH_PIN)

        set_pin(en3Pin,LOW_PIN)
        set_pin(en4Pin,HIGH_PIN)

        set_speed(enAPin,MAX_SPEED)
        set_speed(enBPin,MAX_SPEED)
        time.sleep(MOTOR_START_DELAY)
        set_speed(enAPin,nSpeed)
        set_speed(enBPin,nSpeed)

    def go_back(self):
        set_pin(en1Pin,HIGH_PIN)
        set_pin(en2Pin,LOW_PIN)

        set_pin(en3Pin,HIGH_PIN)
        set_pin(en4Pin,LOW_PIN)

        set_speed(enAPin,MAX_SPEED)
        set_speed(enBPin,MAX_SPEED)
        time.sleep(MOTOR_START_DELAY)
        set_speed(enAPin,nSpeed)
        set_speed(enBPin,nSpeed)
        
    def go_left(self):
        set_pin(en1Pin,HIGH_PIN)
        set_pin(en2Pin,LOW_PIN)

        set_pin(en3Pin,LOW_PIN)
        set_pin(en4Pin,HIGH_PIN)

        set_speed(enAPin,MAX_SPEED)
        set_speed(enBPin,MAX_SPEED)
        time.sleep(MOTOR_START_DELAY)
        set_speed(enAPin,nSpeed)
        set_speed(enBPin,MAX_SPEED)
        
    def go_right(self):
        set_pin(en1Pin,LOW_PIN)
        set_pin(en2Pin,HIGH_PIN)

        set_pin(en3Pin,HIGH_PIN)
        set_pin(en4Pin,LOW_PIN)

        set_speed(enAPin,MAX_SPEED)
        set_speed(enBPin,MAX_SPEED)
        time.sleep(MOTOR_START_DELAY)
        set_speed(enAPin,MAX_SPEED)
        set_speed(enBPin,nSpeed)
    
    def stop(self):
        setSpeed(enAPin, 0);
        setSpeed(enBPin, 0);    


    def set_speed(self, pin, speed):
        if (speed < 0):
            speed = 0
        if (speed > 255):
            speed = 255
        set_pwm(pin, 0, speed*16)    


    def set_normal_speed(self, speed):
        nSpeed = speed;

    def on_buzz(self):
        set_pwm(BuzzPin,0,2048)
    def off_buzz(self):
        setPin(BuzzPin,0)
