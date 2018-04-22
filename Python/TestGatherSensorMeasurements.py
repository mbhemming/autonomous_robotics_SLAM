#!/usr/bin/env python3
import sys
sys.path.insert( 0, '/home/robot/Capstone/Python/Objects' )
sys.path.insert( 0, '/home/robot/Capstone/Python/' )
import ev3dev.ev3 as ev3

import numpy as np
import csv
import FileOutputter as printer
from GatherSensorMeasurements import GatherSensorMeasurements
from ev3dev.ev3 import *

from Robot import Robot
from Point import Point
from RobotPose import RobotPose
from time import sleep
import time
##################INITIALIZATION##################
# Setup the wheel motors
motorRight = ev3.LargeMotor('outA')
motorLeft = ev3.LargeMotor('outD')
motorRight.stop()
motorLeft.stop()

# Setup motor controlling Ultrasonic sensor
motorUltra = ev3.MediumMotor()
motorUltra.stop()

# Setup ultrasonic sensor
# US-DIST-IN range is 0-1003 (1003 is 255 cm)
sensorUltra = ev3.UltrasonicSensor()
sensorUltra.mode = 'US-DIST-IN'

# Setup touch sensor
sensorTouch = ev3.TouchSensor()

start = RobotPose( Point( 0, 0 ), 90 )

bot = Robot( start, motorLeft, motorRight, motorUltra, sensorUltra, sensorTouch )
print( bot )
ev3.Sound.beep().wait()
sleep(0.5)
##################################################
timestr = time.strftime("%Y%m%d-%H%M%S")
with open(timestr+'_TestOutput.csv', 'w') as csvfile:
	data = np.array(GatherSensorMeasurements(50,180,5,sensorUltra,motorUltra))
	printer.AppendToCsv(csvfile, bot, data)
	

