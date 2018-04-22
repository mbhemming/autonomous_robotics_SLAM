#!/usr/bin/env python3
import sys
sys.path.insert( 0, '/home/robot/Capstone/Python/Objects' )
sys.path.insert( 0, '/home/robot/Capstone/Python/' )
import ev3dev.ev3 as ev3
import ev3Functions as func
from Robot import Robot
from Point import Point
from RobotPose import RobotPose


##################INITIALIZATION##################
start = RobotPose( Point( 0, 0 ), 90 )

bot = Robot( start )
print( bot )
##################################################

print( "Continuous" )
for i in range( 0, 100 ):
	print( bot.SUltra.value() )

print( "\n\nDiscrete" )
for i in range( 0, 100 ):
	bot.SUltra.mode = 'US-SI-IN'
	print( bot.SUltra.value() )




