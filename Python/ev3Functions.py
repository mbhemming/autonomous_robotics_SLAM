#!/usr/bin/env python3
import sys
sys.path.insert( 0, './Objects' ) 
import ev3dev.ev3 as ev3
import math
from Robot import Robot
from Point import Point
from RobotPose import RobotPose
from time import sleep
from enum import Enum
doprint = 0
######################ENUMS#######################
class ROTATION(Enum):
	CW = 1
	CCW = 2
##################################################

#####################GLOBALS######################
GEAR_RATIO = 40/8
ROTATION_SPEED = 200

DRIVE_SPEED = 125
SPEED_CONSTANT_CM = 0.007958 # (cm/ms) 
SPEED_CONSTANT_IN = 0.00313307086 # (in/ms) 
##################################################

def ResetMotorPositions( motor1, motor2 ):
	motor1.position_sp = 0
	motor2.position_sp = 0
	
# This function turns the robot to a specified angle using only 1 wheel. 
# This does not look at color values while turning.
def TurnOneWheelDeg( angle, motorLeft, motorRight, wheel ):
	
	# 2.1818 is the ratio of the wheel radius to the robot radius. 
	# The formula is the arc length formula.
	position = 2.1818 * 2 * angle	
	
	if wheel == 'left':
		#turn CW
		motorRight.stop( stop_action = "hold" )
		motorLeft.run_to_rel_pos( position_sp = position, \
								  speed_sp = DRIVE_SPEED, \
								  stop_action = "hold" )
	elif wheel == 'right':
		#turn CCW
		motorLeft.stop( stop_action = "hold" )
		motorRight.run_to_rel_pos( position_sp = position, \
								   speed_sp = DRIVE_SPEED, \
								   stop_action = "hold" )
	else:
		# *Sanity
		print( "invalid wheel", file = sys.error )
		
# This function turns the robot to a specified number of degrees using both 
# wheels.		
def TurnTwoWheelDeg( angle, motorLeft, motorRight ):
	# 2.1818 is the ratio of the wheel radius to the robot radius. 
	# The formula is the arc length formula.
	position = 2.1818 *  angle
	
	# run the motors.
	motorRight.run_to_rel_pos( position_sp = position, speed_sp = DRIVE_SPEED,\
							   stop_action = "hold" )
	motorLeft.run_to_rel_pos( position_sp = -position, speed_sp = DRIVE_SPEED,\
						      stop_action = "hold" )
	motorRight.wait_until_not_moving(timeout=2000)
	motorLeft.wait_until_not_moving(timeout=2000)

# Travel straight for a distance measured in CM. 
def StraightDistCM( dist, motorLeft, motorRight ):
	dtMilli =  dist / ( SPEED_CONSTANT_CM )
	motorLeft.run_to_rel_pos( position_sp = dist*20.83, speed_sp = DRIVE_SPEED , stop_action="hold")	
	motorRight.run_to_rel_pos(position_sp = dist*20.83, speed_sp = DRIVE_SPEED, stop_action="hold" )

	motorLeft.wait_until_not_moving(timeout=dtMilli+500)
	motorRight.wait_until_not_moving(timeout=dtMilli+500)
	if( doprint == 1 ):
		print( "Straight:" )
		print( "  dist: " + str( dist ) )
		print( "  dt: " + str( dtMilli ) ) 

# Travel straight for a distance measured in IN. 
def StraightDistIN( dist, motorLeft, motorRight ):
	dtMilli =  dist / ( SPEED_CONSTANT_IN )
		
	motorLeft.run_to_rel_pos( position_sp = dist*20.83*2.54, speed_sp = DRIVE_SPEED , stop_action="hold")
	motorRight.run_to_rel_pos( position_sp = dist*20.83*2.54, speed_sp = DRIVE_SPEED, stop_action="hold")
 
    
	motorLeft.wait_until_not_moving(timeout=dtMilli+500)
	motorRight.wait_until_not_moving(timeout=dtMilli+500)
	

	if( doprint == 1 ):
		print( "Straight:" )
		print( "  dist: " + str( dist ) )
		print( "  dt: " + str( dtMilli ) ) 

# Calculate angle between current robot angle and desired position
# Arguments:
#     dest: destination point as Point object
#     pose: robot pose as Pose object
# Returns:
#     angle between pose.Theta and vector created from pose.Pt and dest
def CalculateTheta( dest, pose ):
	# formula found on math stack exchange
	# calc current unit vector of robot using current theta
	x1 = math.cos( math.radians( pose.Theta ) ) 
	y1 = math.sin( math.radians( pose.Theta ) )

	# calc vector to travel along.
	x2 = dest.x - pose.Pt.x
	y2 = dest.y - pose.Pt.y 
	
	dot = x1 * x2 + y1 * y2      # dot product
	det = x1 * y2 - y1 * x2      # determinant 

	# atan2(y, x) or atan2(sin, cos )
	return math.degrees( math.atan2( det, dot ) ) 

# Calculate the euclidean distance between pose.Pt and dest
def CalculateDist( dst, src ): 
	dx = src.x - dst.x
	dy = src.y - dst.y
	return math.hypot( dx, dy )
	
# Set the sensor angle to a theta relative to the forward facing position.
def SetSensorAngle( motor, angle ):
	motor.wait_until_not_moving(timeout=1000)
	motor.run_to_abs_pos( position_sp = angle * GEAR_RATIO, \
						  speed_sp = ROTATION_SPEED )

# Return sensor to forward facing position and reset position_sp variable
def ResetSensorAngle( motor ):
	motor.wait_until_not_moving(timeout=1000)
	motor.run_to_abs_pos( position_sp = 0, speed_sp = ROTATION_SPEED )
	motor.position_sp = 0
	return 0

	
