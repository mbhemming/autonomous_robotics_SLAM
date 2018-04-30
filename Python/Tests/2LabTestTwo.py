#!/usr/bin/env python3
import sys
sys.path.append( '../Objects' )
sys.path.append( '../Functions/' )

import ev3dev.ev3 as ev3
import csv
import FileOutputter as printer
from OccupancyGrid import OccupancyGrid
from Robot import Robot
from _Driving import DRIVE_SPEED
from Point import Point
import time

import signal
current_milli_time = lambda: int(round(time.time() * 1000))

print("STARTING")
grid1 = OccupancyGrid(2)
#grid2 = OccupancyGrid(2)
#grid3 = OccupancyGrid(3)
#print("ROBOT: "+ str(grid2.PointToCell(Point(31.0,31.0))))


def signal_handler(signal, frame):
	print('You pressed Ctrl+C!')

	printer.GridToCsv(grid1, "_g1")
#	printer.GridToCsv(grid2, "_g2")

#	printer.GridToCsv(grid3, "_g3")	
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

DRIVE_SPEED = 200
#56 28 26
##################INITIALIZATION################

bot = Robot( 62.0, 0.0 ,90.0 )
print( bot )
ev3.Sound.beep().wait()
time.sleep(0.5)

##################################################
ev3.Sound.beep().wait()
t = current_milli_time()
grid1.INCR_AMOUNT = 15
grid1.DECR_AMOUNT = 24
#grid2.INCR_AMOUNT = 15
#grid2.DECR_AMOUNT = 24
#grid3.INCR_AMOUNT = 15
#grid3.DECR_AMOUNT = 24

Points = [ Point( 62.0, 10.0 ), Point (75.0 , 20.0), Point (75.0, 50.0), Point(12,50), Point(12.0,14.0), Point(68,14.0), Point(66.0,-4.0)]

timestr = time.strftime("%Y%m%d-%H%M%S")
with open('matt_'+timestr+'_TestOutput.csv', 'w') as csvfile:
	for point in Points:
		bot.DriveToPoint( point )
		t = current_milli_time()
		if point.y > 0:
			data = bot.GatherSensorMeasurements2(20,180,15.0,grid1)
			print("time 1inch: " +str(current_milli_time()-t))	
			printer.AppendToCsv(csvfile, bot, data)
#		t = current_milli_time()
#		bot.GatherSensorMeasurements2(20,180,15.0,grid2)
#		print("time 2 inch: " +str(current_milli_time()-t))	
#		t = current_milli_time()
#		data=bot.GatherSensorMeasurements2(20,180,15.0,grid3)
#		print("time 3 inch : " +str(current_milli_time()-t))	
#		printer.AppendToCsv(csvfile, bot, data)



printer.GridToCsv(grid1, "_g1")
#printer.GridToCsv(grid2, "_g2")

#printer.GridToCsv(grid3, "_g3")

#bot.StraightDistIN(-75.0)


