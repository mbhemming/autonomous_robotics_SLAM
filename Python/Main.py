#!/usr/bin/env python3
import ev3dev.ev3 as ev3
from time import sleep
import sys
import math
import ev3Functions as func

motorRight = ev3.LargeMotor('outA')
motorLeft = ev3.LargeMotor('outD')

motorRight.stop()
motorLeft.stop()

ultraSonic = ev3.UltrasonicSensor() 
assert us.connected, "Connect an UltrasonicSensor"
# Put the US sensor into distance mode.
# This goes from 0-1003 (1003 is 255 cm)
us.mode = 'US-DIST-IN'

button = ev3.Button()

current_x = 0
current_y = 0
current_theta = 0.0

func.ResetMotorPositions()
grid_size = 14.8 #cm

doprint = 0 

# REGION: Initialization.
def readArgs():
	if (len (sys.argv) - 1)% 2 != 0 or len(sys.argv) == 1:
		print("INVALID ARGS")
		raise ValueError('Arguments must a series of x y pairs ie: 1 3 2 4 1 5 =(1,3),(2,4),(1,5).')
	destinations = [[0 for x in range(int(round((len(sys.argv)-1)/2)))] for y in range(2)]
	i = 1
	j = 0
	while i < len ( sys.argv ):
		destinations[0][j] = float(sys.argv[i]) * grid_size
		i = i + 1
		destinations[1][j] = float(sys.argv[i]) * grid_size
		i = i + 1
		j = j + 1
	return destinations

def InitCoordinates():
	listy = readArgs()
	print("X,Y Co-ordinate array:")
	print(listy)
	return listy
# END REGION: Initialization.

def do_angle_controller( angle ):
	global motor_A
	global motor_D
	global current_theta

	max_speed = 50

	motor_A.position = 0
	motor_D.position = 0
	
	angleSP = angle * 2.277778
	
	errorA = angleSP
	errorB = -angleSP
	
	kp = 4.0
	kd = 0.01
	ki = 0.5
	
	int_errorA = 0.0
	int_errorB = 0.0
	
	last_error_A = 0.0
	last_error_B = 0.0


	#until error is reduced to within the controllable one encoder tick worth of arc length.
	while ( math.fabs( errorA ) > 1.5 ) or ( math.fabs( errorB ) > 1.5 ):
		errorA = angleSP - motor_A.position
		errorB = -angleSP - motor_D.position

		int_errorA = errorA + int_errorA
		int_errorB = errorB + int_errorB

		der_errorA = errorA - last_error_A
		der_errorB = errorB - last_error_B

		controlSignalA = kp * errorA + ki * int_errorA + kd * der_errorA
		controlSignalB = kp * errorB + ki * int_errorB + kd * der_errorB

		last_error_A = errorA
		last_error_B = errorB

		speed_A = controlSignalA
		speed_D = controlSignalB
		
#cap speed
		
		if speed_A > max_speed:
			int_errorA = 0.0
			speed_A = max_speed
		elif speed_A < -max_speed:
			speed_A = -max_speed
			int_errorA = 0.0

		if speed_D > max_speed:
			speed_D = max_speed
			int_errorB = 0.0
		elif speed_D < -max_speed:
			speed_D = -max_speed
			int_errorB = 0.0
		
		if( doprint == 1 ):
			print( "Dist A: " + str( motor_A.position ) )
			print( "error A: " + str( errorA ) )
			print( "spd A: %d" % ( speed_A ) )
			print( "correct A: %f" % ( controlSignalA ) )
			print( "Dist D: " + str( motor_D.position ) )
			print( "error D: " + str( errorB ) )
			print( "spd D: %d" % ( speed_D ) )
			print( "correc D: %f" % ( controlSignalB ) )
			print( "\n\n\n" )

		motor_A.run_forever( speed_sp = speed_A )
		motor_D.run_forever( speed_sp = speed_D )
		sleep( 0.1 )
	
	motor_A.stop()
	motor_D.stop()
	#Calculate new theta based on current measurements
	dist = ( motor_A.position * 0.0471238898 - motor_D.position * 0.0471238898 ) / 2
	current_theta += math.degrees( dist / 6.15 )
	ev3.Sound.beep()


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

def print_state():
	print( "State: " )
	print( "  x: " + str( current_x ) )
	print( "  y: " + str( current_y ) )
	print( "  theta: " + str( current_theta ) )


#Position Controller For Straight Line.
def do_pos_controller(xdest,ydest):
	global motor_A
	global motor_D
	global current_x
	global current_y 

	motor_A.position = 0
	motor_D.position = 0
	
	DistanceSP = calculate_dist( xdest, ydest )
	
	errorA = DistanceSP
	errorB = DistanceSP

	kp = 100.0
	kd = 1.0
	ki = 5.0

	int_errorA = 0.0
	int_errorB = 0.0
	
	last_error_A = 0.0
	last_error_B = 0.0

	#until error is reduced to within the controllable one encoder tick worth of arc length.
	while ( math.fabs( errorA ) > 0.05 ) or ( math.fabs( errorB ) > 0.05 ):
		distanceWheelA = motor_A.position * 0.0471238898
		distanceWheelB = motor_D.position * 0.0471238898

		errorA = DistanceSP - distanceWheelA
		errorB = DistanceSP - distanceWheelB

		int_errorA = errorA + int_errorA
		int_errorB = errorB + int_errorB

		der_errorA = errorA - last_error_A
		der_errorB = errorB - last_error_B

		controlSignalA = kp * errorA + ki * int_errorA + kd * der_errorA
		controlSignalB = kp * errorB + ki * int_errorB + kd * der_errorB

		last_error_A = errorA
		last_error_B = errorB
		speed_A = controlSignalA
		speed_D = controlSignalB
		
		#cap speed
		if speed_A > 200:
			int_errorA = 0.0
			speed_A = 200
		elif speed_A < -200:
			speed_A = -200
			int_errorA = 0.0

		if speed_D > 200:
			speed_D = 200
			int_errorB = 0.0
		elif speed_D < -200:
			speed_D = -200
			int_errorB = 0.0

		if( doprint == 1 ):
			print( "Dist A: %d" % ( distanceWheelA ) )
			print( "error A: " + str( errorA ) )
			print( "spd A: %d" % ( speed_A ) )
			print( "correct A: %f" % ( controlSignalA ) )
			print( "Dist D: %d" % ( distanceWheelB ) )
			print( "error D: " + str( errorB ) )
			print( "spd D: %d" % ( speed_D ) )
			print( "correc D: %f" % ( controlSignalB ) )
			print( "\n\n\n" )

		motor_A.run_forever( speed_sp = speed_A )
		motor_D.run_forever( speed_sp = speed_D )
		sleep(0.1)
	
	motor_A.stop()
	motor_D.stop()
	#Calculate new x and y based on measured data
	dist = ( motor_A.position * 0.0471238898 + motor_D.position * 0.0471238898 ) / 2
	current_y += dist * math.sin( math.radians( current_theta ) ) 
	current_x += dist * math.cos( math.radians( current_theta ) )
	ev3.Sound.beep()


# start main.

sleep( 1 )

ev3.Sound.beep().wait()

sleep( 1 )

#Read in command line arguments
coordinates = InitCoordinates()	
#

for i in range( len( coordinates[0] ) ):
	# calculate new theta:
	delta_theta = calculate_theta( coordinates[ 0 ][ i ], coordinates[ 1 ][ i ] )
	
	do_angle_controller( delta_theta )
	
	#	calculate delta d = sqrt(dX^2 + dY^2)
	#	straight(d)
	do_pos_controller( coordinates[ 0 ][ i ], coordinates[ 1 ][ i ] )

	print_state()	
		
motor_A.stop()
motor_D.stop()
print("Exiting Happily\n")






