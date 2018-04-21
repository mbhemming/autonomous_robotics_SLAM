#!/usr/bin/env python3
import sys
sys.path.insert(0, '/home/robot/Capstone/Python/Objects')
sys.path.insert(0, '/home/robot/Capstone/Python/')
import ev3dev.ev3 as ev3
from time import sleep
from enum import Enum

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
SPEED_CONSTANT_IN = 0.02021332 # (in/ms) 
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
		
# This function turns the robot to a specified angle using both wheels. 
# This does not look at color values while turning.		
def TurnTwoWheelDeg( angle, motorLeft, motorRight ):
	# 2.1818 is the ratio of the wheel radius to the robot radius. 
	# The formula is the arc length formula.
	position = 2.1818 *  angle
	
	# run the motors.
	motorRight.run_to_rel_pos( position_sp = -position, speed_sp = DRIVE_SPED, \
							stop_action = "hold" )
	motorLeft.run_to_rel_pos( position_sp = position, speed_sp = DRIVE_SPEED, \
						      stop_action = "hold" )

# Travel straight for a distance measured in CM. 
def StraightDistCM( dist, motorLeft, motorRight ):
	dtMilli =  dist / ( SPEED_CONSTANT_CM )
	motorLeft.run_timed( time_sp = dtMilli, speed_sp = DRIVE_SPEED )	
	motorRight.run_timed( time_sp = dtMilli, speed_sp = DRIVE_SPEED )

	motorLeft.wait_while( 'running', dtMilli )
	motorRight.wait_while( 'running', dtMilli )
	if( doprint == 1 ):
		print( "Straight:" )
		print( "  dist: " + str( dist ) )
		print( "  dt: " + str( dtMilli ) ) 

# Travel straight for a distance measured in IN. 
def StraightDistIN( dist, motorLeft, motorRight ):
	dtMilli =  dist / ( SPEED_CONSTANT_IN )
	motorLeft.run_timed( time_sp = dtMilli, speed_sp = DRIVE_SPEED )	
	motorRight.run_timed( time_sp = dtMilli, speed_sp = DRIVE_SPEED )

	motorLeft.wait_while( 'running', dtMilli )
	motorRight.wait_while( 'running', dtMilli )
	if( doprint == 1 ):
		print( "Straight:" )
		print( "  dist: " + str( dist ) )
		print( "  dt: " + str( dtMilli ) ) 

# Calculate angle between current robot angle and desired position
# Arguments:
#     dest: destination point as Point object
#     pose: robot pose as Pose object
def calculate_theta( dest_x, dest_y, cur_theta, cur_x, cur_y ):
	# formula found on math stack exchange
	# calc current unit vector of robot using current theta
	x1 = math.cos( math.radians( current_theta ) ) 
	y1 = math.sin( math.radians( current_theta ) )

	# calc vector to travel along.
	x2 = dest_x - current_x
	y2 = dest_y - current_y 
	
	dot = x1 * x2 + y1 * y2      # dot product
	det = x1 * y2 - y1 * x2      # determinant
	return math.degrees( math.atan2( det, dot ) )  # atan2(y, x) or atan2(sin, cos )

def calculate_dist( dest_x, dest_y ): 
	return math.sqrt( math.pow( current_x - dest_x, 2 ) + math.pow( current_y - dest_y, 2 ) )
	
def set_sensor_angle( motor, angle, direction = ROTATION.CCW ):

	if( direction.value == ROTATION.CW.value ):
		angle = -angle
	
	motor.run_to_rel_pos( position_sp = angle * GEAR_RATIO, speed_sp = ROTATION_SPEED )

def zero_sensor_rotation( motor ):
	motor.run_to_abs_pos( position_sp = 0, speed_sp = 200 )
	motor.position_sp = 0
	return 0

def angle_sweep_for_sensor_readings( rotation_initial, sweep_angle_max, angle_increment, motorRotate, number_of_discrete_sensor_angles, j ):
	#initialize delta_rotation
	delta_rotation = 0;
	
	#Move sensor to furthest angle for sweep
	if( j == 1 ):
		new_pos = rotate_sensor( motor, angle_max )
    
	# Now that max angle has been reached begins sweeping through angles by angle increments 
	if( j > 1 ):
		new_pos = rotate_sensor( motor, angle_increment, ROTATION.CW )

	# This step returns the sensor back to the forward (zero'd postion) 
	if( j > number_of_discrete_sensor_angles ):
		new_pos = zero_sensor_rotation( motor )
	
	return new_pos
