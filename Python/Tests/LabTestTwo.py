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
grid1 = OccupancyGrid(1)
grid2 = OccupancyGrid(2)
grid3 = OccupancyGrid(3)
print("ROBOT: "+ str(grid.PointToCell(Point(31.0,31.0))))

bot = Robot( 61.0, 0.0 ,90.0 )
print( bot )
ev3.Sound.beep().wait()
time.sleep(0.5)

##################################################
ev3.Sound.beep().wait()
t = current_milli_time()
grid.INCR_AMOUNT = 15
grid.DECR_AMOUNT = 24


Points = [ Point( 61.0, 10.0 ), Point (61.0 , 50.0) , Point (50.0, 50.0), Point (16.0, 50.0), Point (16.0, 25.0), Point(60.0, 25.0),Point (60.0, 0.0) ]

for point in Points:
	bot.DriveToPoint( point )
	t = current_milli_time()
	bot.GatherSensorMeasurements(20,180,10.0,grid1)
	print("time 20deg: " +str(current_milli_time()-t))	
	printer.GridToCsv(grid1)
	bot.GatherSensorMeasurements(20,180,10.0,grid2)
	printer.GridToCsv(grid2)
	bot.GatherSensorMeasurements(20,180,10.0,grid3)
	printer.GridToCsv(grid3)
