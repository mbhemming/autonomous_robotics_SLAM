#!/usr/bin/env python3
import sys
sys.path.insert( 0, '/home/robot/Capstone/Python/Objects' )
sys.path.insert( 0, '/home/robot/Capstone/Python/' )
sys.path.insert(0,'./Stats/')
import ev3dev.ev3 as ev3
import SonarStatisticsFunctions as sstats
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
#motorRight = ev3.LargeMotor('outA')
#motorLeft = ev3.LargeMotor('outD')
#motorRight.stop()
#motorLeft.stop()

# Setup motor controlling Ultrasonic sensor
#motorUltra = ev3.MediumMotor()
#motorUltra.stop()

# Setup ultrasonic sensor
# US-DIST-IN range is 0-1003 (1003 is 255 cm)
#sensorUltra = ev3.UltrasonicSensor()
#sensorUltra.mode = 'US-DIST-IN'

# Setup touch sensor
#sensorTouch = ev3.TouchSensor()

start = RobotPose( Point( 0, 0 ), 90 )

bot = Robot( start )
print( bot )
ev3.Sound.beep().wait()
sleep(0.5)
##################################################
timestr = time.strftime("%Y%m%d-%H%M%S")
with open(timestr+'_TestOutput.csv', 'w') as csvfile:
	for i in range(0,5):
		data = np.array(GatherSensorMeasurements(150,180,5,bot.SUltra,bot.MUltra))
		#sstats.DecomposeSonarReadings(data,0)
		printer.AppendToCsv(csvfile, bot, data)
		bot.DriveToPoint(Point(0,6*(i+1)))


