#!/usr/bin/env python3
import sys
sys.path.append( '../Objects' )
sys.path.append( '../Objects/Robot' )
from Robot.Robot import Robot
from Point import Point
from Pose import Pose

# POINT
print( "TESTING POINT" )
p = Point( 1.2, 1.1 )
print( p )
print( str( p.x ) )
print( str( p.y ) )
print( "POINT TEST COMPLETE\n\n" )


# POSE
print( "TESTING POSE" )
ps = Pose( 7.9, 87, 32 )
print( ps )
print( str( ps.x ) )
print( str( ps.y ) )
print( str( ps.Theta ) )
print( "POSE TEST COMPLETE\n\n" )

# ROBOT
print( "TESTING ROBOT" )
r = Robot( 10.9, 8.7, 132 )
print( r )
print( "DriveToPoint" )
r.DriveToPoint( Point( 17, 3 ) )
print( "TurnOneWheelDeg" )
r.TurnOneWheelDeg( -150, 'right' )
r.TurnOneWheelDeg( 150, 'left' )
print( "TurnTwoWheelDeg" )
r.TurnTwoWheelDeg( 45 )
print( "StraightDistCM" )
r.StraightDistCM( -50 )
print( "StraightDistIN" )
r.StraightDistIN( 10 )
print( "CalculateTheta" )
r.CalculateTheta( Point( 4, 13 ) )
print( "SetSensorAngle" )
r.SetSensorAngle( 35 )
print( "ResetSensorAngle" )
r.ResetSensorAngle()
print( "ROBOT TEST COMPLETE\n\n" )


