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
grid0 = OccupancyGrid(24,28,3)
grid1 = OccupancyGrid(24,28,3)
grid2 = OccupancyGrid(24,28,3)
grid3 = OccupancyGrid(24,28,3)

print("ROBOT: "+ str(grid0.PointToCell(Point(31.0,31.0))))

bot = Robot( 31.0,31.0,90.0 )
print( bot )
ev3.Sound.beep().wait()
time.sleep(0.5)

##################################################
#timestr = time.strftime("%Y%m%d-%H%M%S")
#with open(timestr+'_TestOutput.csv', 'w') as csvfile:
for k in range (0,8):
    ev3.Sound.beep().wait()
    t = current_milli_time()
    bot.GatherSensorMeasurements(20,180,10,grid0)
    print("time 10deg: " +str(current_milli_time()-t))

for i in range(0,8):
    ev3.Sound.beep().wait()
    t = current_milli_time()
    bot.GatherSensorMeasurements(20,180,15, grid1)
    print("time 15deg: " +str(current_milli_time()-t))

for j in range(0,8):
    ev3.Sound.beep().wait()
    t = current_milli_time()
    bot.GatherSensorMeasurements(20,180,20, grid2)
    print("time 20deg: " +str(current_milli_time()-t))

for i in range(0,8):
    ev3.Sound.beep().wait()
    t = current_milli_time()
    bot.GatherSensorMeasurements(20,180,25, grid3)
    print("time 25deg: " +str(current_milli_time()-t))

printer.GridToCsv(grid0)
printer.GridToCsv(grid1)
printer.GridToCsv(grid2)
printer.GridToCsv(grid3)
