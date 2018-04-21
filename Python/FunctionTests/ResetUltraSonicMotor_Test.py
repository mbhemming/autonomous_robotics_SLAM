#!/usr/bin/env python3
import sys
sys.path.insert(0, '/home/robot/Capstone/Python')
import ev3dev.ev3 as ev3
import ev3Functions as func
from time import sleep


motorUltraSonic = ev3.MediumMotor()
assert motorUltraSonic.connected

print( func.zero_sensor_rotation( motorUltraSonic ) )

motorUltraSonic.wait_until_not_moving()

sleep(2)


