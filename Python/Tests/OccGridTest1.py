#!/usr/bin/env python3
import sys
sys.path.insert(0,'../Objects')
sys.path.insert( 0, '../Functions/' )

import ev3dev.ev3 as ev3
import numpy as np
import csv
import FileOutputter as printer
from OccupancyGrid.OccupancyGrid import OccupancyGrid
from Robot.Robot import Robot
import time
##################INITIALIZATION################

grid = OccupancyGrid(24,28,3)
bot = Robot( 0.0,0.0,90.0 )
print( bot )
ev3.Sound.beep().wait()
time.sleep(0.5)

##################################################
timestr = time.strftime("%Y%m%d-%H%M%S")
with open(timestr+'_TestOutput.csv', 'w') as csvfile:
		data = np.array(bot.GatherSensorMeasurements(50,180,5, grid))	
		printer.AppendToCsv(csvfile, bot, data)

