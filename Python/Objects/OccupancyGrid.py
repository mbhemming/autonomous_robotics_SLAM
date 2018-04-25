import numpy as np
from Point import Point
from Pose import Pose
from _OccupancyGrid import _OccupancyGrid
        
class OccupancyGrid( _OccupancyGrid ):
    MAX_PROB = 100
    MIN_PROB = 0
    COURSE_Y_IN= 69.75
    COURSE_X_IN= 81.5
    DOOR_START_IN = 52.0
    DOOR_END_IN = 70.25

    def __init__( self, cellWidth ):
        self.Rows = int( self.COURSE_Y_IN / cellWidth ) + 1
        self.Cols = int( self.COURSE_X_IN / cellWidth ) + 1
        self.CellWidth = cellWidth
        # Define the walls as max probability of object (shouldnt be changed)
        self.Grid = np.zeros( ( self.Rows, self.Cols ), dtype = int )
        self.Grid[ 0, : ] = self.MAX_PROB
        self.Grid[ :, 0 ] = self.MAX_PROB
        self.Grid[ self.Rows - 1, : ] = self.MAX_PROB
        self.Grid[ :, self.Cols - 1 ] = self.MAX_PROB
        # Remove the door from the wall grid.
        for col in range( int( self.DOOR_START_IN / self.CellWidth ) + 1,\
                          int( self.DOOR_END_IN / self.CellWidth ) ):
            self.Grid[ 0, col ] = self.MIN_PROB
        
    def Specs( self ):
        return "Rows: " + str( self.Rows ) + "\nCols: " + str( self.Cols ) +\
               "\nCell Width: " + str( self.CellWidth )

    def UpdateProb( self, row, col, prob ):
        if( not self.IsWall( row, col ) ):
            if( prob > self.MAX_PROB ):
                prob = self.MAX_PROB

            if( prob < self.MIN_PROB ):
                prob = self.MIN_PROB

            self.Grid[ row, col ] = prob

    def IncProbCell(self, row, col):
        if( not self.IsWall( row, col ) ):
            self.Grid[ row, col ] += 5
            if( self.Grid[ row, col ] > self.MAX_PROB ):
                self.Grid[ row, col ] = self.MAX_PROB

    def IncProbCells( self, cells ):
        for cell in cells:
            self.IncProbCell( cell[ 0 ], cell[ 1 ] )

    def DecProbCell(self, row, col):
        if( not self.IsWall( row, col ) ):
            self.Grid[ row, col ] -= 8
            if( self.Grid[ row, col ] < self.MIN_PROB ):
                self.Grid[ row, col ] = self.MIN_PROB

    def DecProbCells( self, cells ):
        for cell in cells:
            self.DecProbCell( cell[ 0 ], cell[ 1 ] )

    def CellToPoint( self, r, c ):
        return Point( self.CellWidth * ( c + 0.5 ), self.CellWidth * ( r + 0.5 ) )

    def PointToCell( self, pt ):
        return ( int( pt.y / self.CellWidth ), int( pt.x / self.CellWidth ) )
   
    def IsWall( self, row = 0, col = 0 ):
        return row == 0 or row == self.Rows - 1 or col == 0 or col == self.Cols - 1

    # Rounds a point to the center point of a cell 
    def RoundPoint( self, pt ):
        cell = self.PointToCell( pt )
        return self.CellToPoint( cell[ 0 ], cell[ 1 ] )
























