
class Robot:
		
	def __init__( self, pose, motorLeft, motorRight, motorUltra, sensorUltra, \
				  sensorTouch ):
		self.Pose = pose
		self.MLeft = motorLeft
		self.MRight = motorRight
		self.MUltra = motorUltra
		self.SUltra = sensorUltra
		self.STouch = sensorTouch
	
	def __str__(self):
		return str( self.Pose ) + "\nMotors: \n  Left: " +\
			   str( self.MLeft.connected ) + "\n  Right: " +\
			   str( self.MRight.connected ) + "\n  Ultra: " +\
			   str( self.MUltra.connected ) + "\nSensors: \n  Ultra: " +\
			   str( self.SUltra.connected ) + "\n  Touch: " +\
			   str( self.STouch.connected ) + "\n"
