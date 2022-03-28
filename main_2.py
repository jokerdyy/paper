# Servo Shield Example.
#
# This example demonstrates the servo shield. Please follow these steps:
#
#   1. Connect a servo to any PWM output.
#   2. Connect a 3.7v battery (or 5V source) to VIN and GND.
#   3. Copy pca9685.py and servo.py to OpenMV and reset it.
#   4. Connect and run this script in the IDE.

import time
from servo import Servos
from machine import I2C, Pin

i2c = I2C(sda=Pin('P5'), scl=Pin('P4'))
servo = Servos(i2c, address=0x40, freq=50, min_us=650, max_us=2800, degrees=180)

while True:
    servo.position(0, 60)
    time.sleep(1500)
    servo.position(1, 30)
    time.sleep(1500)
    servo.position(2, 0)
    time.sleep(1500)
    servo.position(3, 8)
    time.sleep(3500)
    servo.position(0, 60)
    time.sleep(1500)
    servo.position(1, 25)
    time.sleep(1500)
    servo.position(2, 10)
    time.sleep(1500)
    servo.position(3, 60)
    time.sleep(500)
    break
