
from __future__ import division
import time

# Import the PCA9685 module.
import rasp_car_PCA9685 as pca


# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
pwm = pca.PCA9685()


while True:
    # Move servo on channel O between extremes.
    pwm.set_pwm(0, 0, 1000)
    time.sleep(1)
    pwm.set_pwm(0, 0, 500)
    time.sleep(1)
