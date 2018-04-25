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
grid = OccupancyGrid(2)
grid2 = OccupancyGrid(2)
print("ROBOT: "+ str(grid.PointToCell(Point(31.0,31.0))))

bot = Robot( 31.0,31.0,90.0 )
print( bot )
ev3.Sound.beep().wait()
time.sleep(0.5)

##################################################
ev3.Sound.beep().wait()
t = current_milli_time()
grid.INCR_AMOUNT = 15
grid.DECR_AMOUNT = 24
bot.GatherSensorMeasurements(20,180,15,grid)
print("time 20deg: " +str(current_milli_time()-t))
printer.GridToCsv(grid)
grid2.INCR_AMOUNT = 18
grid2.DECR_AMOUNT = 24
bot.GatherSensorMeasurements(20,180,15,grid2)
printer.GridToCsv(grid)


bot.DriveToPoint( Point(31.0, 35.0) )
t = current_milli_time()
bot.GatherSensorMeasurements(20,180,15,grid)
print("time 20deg: " +str(current_milli_time()-t))
printer.GridToCsv(grid)
bot.GatherSensorMeasurements(20,180,15,grid2)
printer.GridToCsv(grid2)


bot.DriveToPoint( Point(31.0, 39.0) )
t = current_milli_time()
bot.GatherSensorMeasurements(20,180,15,grid)
print("time 20deg: " +str(current_milli_time()-t))
printer.GridToCsv(grid)
bot.GatherSensorMeasurements(20,180,15,grid2)
printer.GridToCsv(grid2)

bot.DriveToPoint( Point(31.0, 44.0) )
t = current_milli_time()
bot.GatherSensorMeasurements(20,180,15,grid)
print("time 20deg: " +str(current_milli_time()-t))
printer.GridToCsv(grid)
bot.GatherSensorMeasurements(20,180,15,grid2)
printer.GridToCsv(grid2)


