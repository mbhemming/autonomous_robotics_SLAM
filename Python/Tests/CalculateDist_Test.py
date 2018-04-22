#!/usr/bin/env python3
import sys
sys.path.insert(0, '/home/robot/Capstone/Python')
sys.path.insert(0, '/home/robot/Capstone/Python/Objects')
import ev3Functions as func
from Point import Point
from RobotPose import RobotPose

src = Point( 2.5, 7 )
dest = Point( 0, 3 )

print( func.CalculateDist( dest, src ) )

src = Point( 7.93, 15.156 )
dest = Point( 18.436, 2.781 )

print( func.CalculateDist( dest, src ) )

