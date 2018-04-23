import sys
sys.path.append( '../' )

from Point import Point 

class GridCell:

    def __init__( self, r = 0, c = 0, prob = 0 ):
        self.Row = r
        self.Col = c
        self.Prob = prob
        self.Width = 3
        
    def ToPoint( self ):
        return Point( self.Col * self.Width + 1.5, self.Row * self.Width + 1.5 )

