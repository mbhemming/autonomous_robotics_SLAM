#!/usr/bin/env python3
import sys
sys.path.insert( 0, '/home/robot/Capstone/Python/Objects' )
sys.path.insert( 0, '/home/robot/Capstone/Python/' )
import ev3dev.ev3 as ev3
import ev3Functions as func
from Robot import Robot
from Point import Point
from RobotPose import RobotPose
from time import sleep

##################INITIALIZATION##################
start = RobotPose( Point( 0, 0 ), 90 )

bot = Robot( start )
print( bot )
##################################################

print( "Continuous " + bot.SUltra.mode )
for i in range( 0, 1000 ):
    bot.SUltra.mode = 'US-DIST-IN'
    print( bot.SUltra.value() )
    bot.SUltra.mode = 'US-LISTEN'
    if( bot.SUltra.value() ):
        print( "!!!!!!!!!!" )
