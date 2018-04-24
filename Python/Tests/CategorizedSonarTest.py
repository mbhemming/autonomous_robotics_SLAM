#!/usr/bin/env python3
import sys
sys.path.append( '../Objects' )
sys.path.append( '../Python/' )

import ev3dev.ev3 as ev3
import SonarStatisticsFunctions as sstats
import numpy as np
import csv
import FileOutputter as printer
from GatherSensorMeasurements import GatherSensorMeasurements

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
	for i in range(0,5):
		data = np.array( bot.GatherSensorMeasurements( 50, 180, 5 ) )
		printer.AppendToCsv(csvfile, bot, data)
		bot.DriveToPoint(Point(0,6*(i+1)))


