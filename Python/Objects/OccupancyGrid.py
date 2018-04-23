import math
import numpy as np
from Point import Point
		
class OccupancyGrid:
		
	def __init__( self ):
		self.occupancyGrid = np.zeros( ( 24, 28 ), dtype = np.bool_ )
		self.occupancyGrid[ 0, : ] = True
		self.occupancyGrid[ :, 0 ] = True
		self.occupancyGrid[ 23, : ] = True
		self.occupancyGrid[ :, 28 ] = True
		
	def UpdateOccupancy( self, x, y, isOccupied ):
		row = math.floor( y )
		col = math.floor( x )
		self.occupancyGrid[ row, col ] = isOccupied
		
	def XYOccupied( self, x, y ):
		row = math.floor( y )
		col = math.floor( x )
		return self.occupancyGrid[ row, col ]
    
    def CellToPoint( r, c ):
        return Point( c * 3 + 1.5, r * 3 + 1.5 )

    def PointToCell( pt ):
        return ( int( pt.y / 3 ), int( pt.x / 3 ) )

