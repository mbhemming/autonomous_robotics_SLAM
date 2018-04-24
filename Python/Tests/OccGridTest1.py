#!/usr/bin/env python3
import sys
sys.path.append( '../Objects' )
sys.path.append( '../Functions/' )

import ev3dev.ev3 as ev3
import csv
import FileOutputter as printer
from OccupancyGrid import OccupancyGrid
from Robot import Robot
import time
##################INITIALIZATION################

grid = OccupancyGrid(24,28,3)
bot = Robot( 30.0,30.0,90.0 )
print( bot )
ev3.Sound.beep().wait()
time.sleep(0.5)

##################################################
#timestr = time.strftime("%Y%m%d-%H%M%S")
#with open(timestr+'_TestOutput.csv', 'w') as csvfile:
for i in range(0,8):
	print(str(i))
	bot.GatherSensorMeasurements(10,180,15, grid)
#		printer.AppendToCsv(csvfile, bot, data)
printer.GridToCsv(grid)
