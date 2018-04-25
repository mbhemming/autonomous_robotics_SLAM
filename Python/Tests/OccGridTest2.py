#!/usr/bin/env python3
import sys
sys.path.append( '../Objects' )
sys.path.append( '../Functions/' )

import ev3dev.ev3 as ev3
import csv
import FileOutputter as printer
from OccupancyGrid import OccupancyGrid
from Robot import Robot
from Point import Point
import time
##################INITIALIZATION################
current_milli_time = lambda: int(round(time.time() * 1000))
grid = OccupancyGrid(3)

print("ROBOT: "+ str(grid.PointToCell(Point(31.0,31.0))))

bot = Robot( 31.0,31.0,90.0 )
print( bot )
ev3.Sound.beep().wait()
time.sleep(0.5)

##################################################
ev3.Sound.beep().wait()
t = current_milli_time()
bot.GatherSensorMeasurements(20,180,10,grid)
print("time 10deg: " +str(current_milli_time()-t))
printer.GridToCsv(grid)
