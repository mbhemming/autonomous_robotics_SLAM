#!/usr/bin/env python3
import sys
sys.path.insert( 0, '/home/robot/Capstone/Python/Objects' )
sys.path.insert( 0, '/home/robot/Capstone/Python/' )
import ev3dev.ev3 as ev3
import ev3Functions as func
from GatherSensorMeasurements import GatherSensorMeasurements
from Robot import Robot
from Point import Point
from RobotPose import RobotPose
from time import sleep
##################INITIALIZATION##################
# Setup the wheel motors
motorRight = ev3.LargeMotor('outA')
motorLeft = ev3.LargeMotor('outD')
motorRight.stop()
motorLeft.stop()

# Setup motor controlling Ultrasonic sensor
motorUltra = ev3.MediumMotor()
motorUltra.stop()

# Setup ultrasonic sensor
# US-DIST-IN range is 0-1003 (1003 is 255 cm)
sensorUltra = ev3.UltrasonicSensor() 
sensorUltra.mode = 'US-DIST-IN'

# Setup touch sensor
sensorTouch = ev3.TouchSensor()

start = RobotPose( Point( 0, 0 ), 90 )

bot = Robot( start, motorLeft, motorRight, motorUltra, sensorUltra, sensorTouch )
print( bot )
ev3.Sound.beep().wait()
sleep(0.5)
##################################################


bot.DriveToPoint( Point( 12, 12 ) )
data = GatherSensorMeasurements( 5, 180, 15, sensorUltra, motorUltra )
print( bot )
print( data )

bot.DriveToPoint( Point( -12, 12 ) )
data = GatherSensorMeasurements( 5, 180, 15, sensorUltra, motorUltra )
print( bot )
print( data ) 


bot.DriveToPoint( Point( 0, 0 ) )
data = GatherSensorMeasurements( 5, 180, 15, sensorUltra, motorUltra )
print( bot )
print( data )



