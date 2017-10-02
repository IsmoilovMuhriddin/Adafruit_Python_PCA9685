# Adafruit Python PCA9685
Python code to use the PCA9685 PWM for Motor control of Smart Car

## Installation

To install the library from source (recommended) run the following commands on a Raspberry Pi or other Debian-based OS system:

    sudo apt-get install git build-essential python-dev
    cd ~
    git clone https://github.com/IsmoilovMuhriddin/Adafruit_Python_PCA9685.git
    cd Adafruit_Python_PCA9685
    sudo python setup.py install

## Requirements
wiringpi

    sudo pip install wiringpi

## Functions
helper functions
    set_pwm_freq(freq_hz)
    set_pwm(channel,on,off)
    set_all_pwm(on,off)
    set_pin(pin,value)

car control
    go_forward()
    go_back()
    go_left()
    go_right()
    stop()
    set_speed(pin,speed)
    set_normal_speed(speed)
    on_buzz()
    off_buzz()
