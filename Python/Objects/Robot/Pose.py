import sys
sys.path.append( '../' )

from Point import Point 
    
class Pose( Point ):
    
    def __init__( self, x=float('nan'), y=float('nan'), theta=float('nan') ):
        if isinstance( x, list ) or  isinstance( x, tuple ):
            self.Theta = x[ 2 ]
            super().__init__( x[ 0 ], x[ 1 ] )
        elif isinstance( x, Pose ):
            self.Theta = x.Theta
            super().__init__( x.x, x.y )
        elif isinstance( x, Point ):
            self.Theta = y
            super().__init__( x.x, x.y )
        else:
            self.Theta = theta
            super().__init__( x, y )
    
    def __str__(self):
        return "Pos: " + super().__str__() + "\nTheta: " + str( self.Theta )
