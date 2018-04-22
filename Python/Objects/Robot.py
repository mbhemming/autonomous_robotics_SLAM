import sys
sys.path.insert(0,'../')

import ev3Functions as ev3f
from RobotPose import RobotPose

class Robot:
		
	def __init__( self, pose, motorLeft, motorRight, motorUltra, sensorUltra, \
				  sensorTouch ):
		self.Pose = pose
		self.MLeft = motorLeft
		self.MRight = motorRight
		self.MUltra = motorUltra
		self.SUltra = sensorUltra
		self.STouch = sensorTouch
		assert self.MLeft.connected, "Left motor not connected"
		assert self.MRight.connected, "Right motor not connected" 
		assert self.MUltra.connected, "Ultrasonic (medium) motor not connected"
		assert self.SUltra.connected, "Ultrasonic sensor not connected"
		assert self.STouch.connected, "Touch sensor not connected"
		ev3f.ResetSensorAngle(self.MUltra)
	
	def __str__( self ):
		return str( self.Pose )
 
	def DriveToPoint( self, dest ):
	    # calculate new theta:
		delta_theta = ev3f.CalculateTheta( dest, self.Pose )
		ev3f.TurnTwoWheelDeg( delta_theta, self.MLeft, self.MRight )

    	#   calculate delta d = sqrt(dX^2 + dY^2)
	    #   straight(d)
		ev3f.StraightDistIN( ev3f.CalculateDist( dest, self.Pose.Pt ),\
							 self.MLeft, self.MRight )
		self.Pose.Pt.x = dest.x
		self.Pose.Pt.y = dest.y
		self.Pose.Theta += delta_theta
