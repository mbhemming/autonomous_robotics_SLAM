import Point 
	
class RobotPose:
		
	def __init__( self, pt, theta ):
		self.Pt = pt
		self.Theta = theta
	
	def __str__(self):
		return "Pos: " + str( self.Pt ) + "\nTheta: " + str( self.Theta )
