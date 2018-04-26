#!/usr/bin/env python3
import sys
sys.path.append('./Objects' )
sys.path.append('./Functions' )
import ev3dev.ev3 as e
from Robot import Robot
from Point import Point
from OccupancyGrid import OccupancyGrid
from time import sleep
import FileOutputter as printer 

##################INITIALIZATION##################

button = e.Button()

csvfile = open( 'rawSonarData.csv', 'w' )

bot = Robot( 61.1, -4.5, 90 )
occGrid = OccupancyGrid( 1 )

waypoints = [ Point( 61.1, 49.75 ),\
              Point( 12, 49.75 ),\
              Point( 12, 12 ),\
              Point( 61.1, 12 ) ] 

##################################################

e.Sound.beep()
while not button.any():
    sleep( 0.01 )

sleep( 5 )

bot.StraightDistIN( 12 + 4.5 )
data = bot.GatherSensorMeasurements2( 30, 180, 5, occGrid )
printer.AppendToCsv( csvfile, bot, data )

for p in waypoints:
    res = bot.DriveToPoint( p, occGrid )
    print( res )
    data = bot.GatherSensorMeasurements2( 30, 180, 5, occGrid )
    printer.AppendToCsv( csvfile, bot, data )

bot.TurnTwoWheelDeg( -( 90 + bot.Theta ) )
bot.StraightDistIn( 24 )
printer.GridToCsv( occGrid )

