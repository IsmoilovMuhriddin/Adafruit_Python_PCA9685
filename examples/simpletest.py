
from __future__ import division
import time

# Import the PCA9685 module.
import rasp_car_PCA9685 as pca


# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
pca9685 = pca.PCA9685()


while True:
    # Move servo on channel O between extremes.
    pca9685.go_forward();
	time.sleep(20);
	pca9685.stop();
	pca9685.go_back();
	time.sleep(20);
	pca9685.stop();
