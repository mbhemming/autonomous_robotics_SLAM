#!/usr/bin/env python3
import sys
sys.path.insert(0, '/home/robot/Capstone/Python')
sys.path.insert(0, '/home/robot/Capstone/Python/Objects')
import ev3Functions as func
from Point import Point
from RobotPose import RobotPose

pose = RobotPose( Point( 1.5, 1 ), 0 )
dest = Point( 1, 1.5 )

print( func.CalculateTheta( dest, pose ) )

pose = RobotPose( Point( 2, 3.25 ), 45 )
dest = Point( 0.25, 1.5 )

print( func.CalculateTheta( dest, pose ) )

