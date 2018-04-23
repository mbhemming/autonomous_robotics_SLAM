import sys
sys.path.insert(0,'./Robot/')
import math
from Point import Point
from Pose import Pose

def GetOccupationUpdate( robopose, sonarReturn, sonarCenterAngleRel , aRes, assumedConeAngle, dRes):
	roboPose = Pose(robopose)
	sonarCenterAngle = sonarCenterAngleRel +roboPose.Theta
	startAngle = sonarCenterAngle - (assumedConeAngle/2.0)
	
	x0 = roboPose.x
	y0 = roboPose.y
	print ("x: " + str(x0))
	print ("y: " + str(y0))
	print ("t: " + str(sonarCenterAngle))

	for i in range(0, math.floor(assumedConeAngle/aRes) + 1):
		
		theta =  startAngle + (i*aRes)
		#print ("Theta: " + str(theta))
		endPoint = Point( x0 + sonarReturn*math.cos(theta), y0 + sonarReturn*math.sin(theta))
		print("Ends at: " + str(endPoint))
		
	
	
	

