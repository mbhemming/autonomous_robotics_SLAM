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
start = RobotPose( Point( 0, 0 ), 90 )

bot = Robot( start )
print( bot )
ev3.Sound.beep().wait()
sleep(0.5)
##################################################
timestr = time.strftime("%Y%m%d-%H%M%S")
with open(timestr+'_TestOutput.csv', 'w') as csvfile:
	data = np.array(GatherSensorMeasurements(50,180,5,bot.SUltra,bot.MUltra))
	printer.AppendToCsv(csvfile, bot, data)
	

