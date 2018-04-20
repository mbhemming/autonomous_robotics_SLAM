from enum import Enum
class ROTATION(Enum):
	CW = 1
	CCW = 2
    
def ResetMotorPositions():
	global motorRight
	global motorLeft
	motorRight.position = 0
	motorLeft.position = 0
	
# This function turns the robot to a specified angle using only 1 wheel. 
# This does not look at color values while turning.
def TurnDeg( angle, wheel ):
	speed = 125 # Arbitrary number determined by trial and error
	
	# 2.1818 is the ratio of the wheel radius to the robot radius. 
	# The formula is the arc length formula.
	position = 2.1818 * 2 * angle	
	
	if wheel == 'left':
		#turn CW
		motor_A.stop( stop_action = "hold" )
		motor_D.run_to_rel_pos( position_sp = position, speed_sp = speed, stop_action = "hold" )
	elif wheel == 'right':
		#turn CCW
		motor_D.stop( stop_action = "hold" )
		motor_A.run_to_rel_pos( position_sp = position, speed_sp = speed, stop_action = "hold" )
	else:
		# *Sanity
		print( "invalid wheel", file = sys.error )
		
# This function turns the robot to a specified angle using both wheels. 
# This does not look at color values while turning.		
def TurnDegTwoWheel( angle ):
	speed = 125 	# Arbitrary number determined by trial and error
	
	# 2.1818 is the ratio of the wheel radius to the robot radius. 
	# The formula is the arc length formula.
	position = 2.1818 *  angle
	
	# run the motors.
	motor_A.run_to_rel_pos(position_sp = ((-1.0) *position), speed_sp = speed, stop_action = "hold" )
	motor_D.run_to_rel_pos( position_sp = position, speed_sp = speed, stop_action = "hold" )
	
# This function turns the robot 90 degrees CCW while watching the colour values from the sensor. If the colour value
# is within the hysteresis band, the motor is stopped and a True value is returned. If the value never reaches the 
# hysteresis band, the robot is returned to its original position and a False value is returned. 
def CCW_sweep():
	global value
	
	print(" CCW Sweep.\n")
	
	TurnDeg( angle = 100, wheel = 'right' )
	
	while motor_A.is_running:
		# Read colour sensor.
		value = cs.value()
		
		if value < hyst_high and value > hyst_low:
			# Tape found
			motor_A.stop()
			return True
		
		sleep( 0.01 ) # sanity
	
	# Tape not found
	TurnDeg( angle = -100, wheel = 'right' )
	
	motor_A.wait_while('running')
	return False

# This function turns the robot 90 degrees CW while watching the colour values from the sensor. If the colour value
# is within the hysteresis band, the motor is stopped and a True value is returned. If the value never reaches the 
# hysteresis band, the robot is returned to its original position and a False value is returned. 
def CW_sweep():
	global value
	
	print(" CW Sweep.\n")
	
	TurnDeg( angle = 100, wheel = 'left' )
	
	while motor_D.is_running:
		# Read colour sensor.
		value = cs.value()
		
		if value < hyst_high and value > hyst_low:
			# Tape found
			motor_D.stop()
			return True
		
		sleep( 0.01 ) # sanity
		
	# Tape not found
	TurnDeg( angle = -100, wheel = 'left' )
	
	motor_D.wait_while('running')
	return False

# This function drives the robot straight a specified number of CM while watching the colour values from the sensor. 
# If the colour value is within the hysteresis band, the motors are stopped and a True value is returned. If the value 
# never reaches the hysteresis band, a False value is returned. 
def straight_cm_sweep( dist ):
	global value
	
	print(" Straight search along %d cm.\n" % dist)	
	
	speed = 100 # Arbitrary speed chosen by trial and error.
	
	#20.83 is derived from arc length formula
	motor_A.run_to_rel_pos( position_sp = dist * 20.83, speed_sp = speed, stop_action = "hold" )
	motor_D.run_to_rel_pos( position_sp = dist * 20.83, speed_sp = speed, stop_action = "hold" )
	
	while motor_A.is_running:
		# Read colour sensor
		value = cs.value()
		
		sleep(0.01) # sanity
		
		if value < hyst_high:
			# Tape found, stop motors
			motor_A.stop()
			motor_D.stop()
			return True
			
	#tape not found, motors already stopped. 
	return False
	
def straight_cm( dist ):
	dtMilli =  dist / ( SPEED_CONSTANT )
	motor_A.run_timed( time_sp = dtMilli, speed_sp = speed )	
	motor_D.run_timed( time_sp = dtMilli, speed_sp = speed )
#	if( dtMilli != 0.0 ):
	motor_A.wait_while( 'running', dtMilli )
	motor_D.wait_while( 'running', dtMilli )
	if( doprint == 1 ):
		print( "Straight:" )
		print( "  dist: " + str( dist ) )
		print( "  dt: " + str( dtMilli ) ) 

def calculate_theta( dest_x, dest_y ):
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
	
def rotate_sensor( angle, direction = ROTATION.CW ):
function [ current_sensor_angle ] = angle_sweep( rotation_initial, sweep_angle_max, angle_increment, j, ...
motorRotate )

	%gear ratio of sensor
	gear_ratio = 40/8;
	rotate_speed = 20;

motorRotate.Speed = rotate_speed;
delta_rotation = 0;

%Move sensor to furthest angle for sweep
if ( j == 1 )
    rotate_angle = sweep_angle_max;
    
    while( abs( delta_rotation ) < rotate_angle * gear_ratio );
        rotation = readRotation( motorRotate );
        delta_rotation = abs( rotation - rotation_initial );
        start( motorRotate );    
    end
    
end
    
stop( motorRotate )

if ( j > 1 )
    delta_rotation = 0;
    motorRotate.Speed = -rotate_speed;

    rotation_initial_temp = readRotation(motorRotate);

    while ( abs(delta_rotation) < angle_increment*gear_ratio )
        rotation = readRotation(motorRotate);
        delta_rotation = abs( rotation - rotation_initial_temp );
        start( motorRotate );    
    end

    stop( motorRotate ) 

end
    
current_sensor_angle = (readRotation(motorRotate) - rotation_initial)/gear_ratio;
if current_sensor_angle < 0
    current_sensor_angle = 360+current_sensor_angle;
else
    
end

end