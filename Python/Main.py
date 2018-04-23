#!/usr/bin/env python3
import sys
sys.path.append('./Objects' )
sys.path.append('./Objects/Robot' )
#import ev3dev.ev3 as ev3
#import ev3Functions as func
from Robot.Robot import Robot
#from Point import Point
from RobotPose import RobotPose

##################INITIALIZATION##################
start = RobotPose( Point( 0, 0 ), 90 )

bot = Robot( start )
print( bot )
##################################################
