import sys
sys.path.append( '../' )

import Point 
	
class Pose( Point.Point ):
	
    def __init__( self, x, y, theta ):
        self.Theta = theta
        super().__init__( x, y )
#        self.x = pt.x
#        self.y = pt.y
	
    def __str__(self):
        return "Pos: " + super().__str__() + "\nTheta: " + str( self.Theta )
