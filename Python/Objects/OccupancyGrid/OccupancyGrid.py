import numpy as np
from Robot.Pose import Pose
from OccupancyGrid._OccupancyGrid import _OccupancyGrid
        
class OccupancyGrid( _OccupancyGrid ):
    MAX_PROB = 100
    MIN_PROB = 0

    def __init__( self, rows, cols, cellWidth ):
        self.Rows = rows
        self.Cols = cols
        self.CellWidth = cellWidth
        self.Grid = np.zeros( ( rows, cols ), dtype = int )
        self.Grid[ 0, : ] = self.MAX_PROB
        self.Grid[ :, 0 ] = self.MAX_PROB
        self.Grid[ rows - 1, : ] = self.MAX_PROB
        self.Grid[ :, cols - 1 ] = self.MAX_PROB
        
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

    def IncProb( self, row = int( 0 ), col = int( 0 ) ):
        if( isinstance( row, list ) ):
            for cell in row:
                self.IncProb( cell[ 0 ], cell[ 1 ] )
        elif( not self.IsWall( row, col ) ):
            self.Grid[ row, col ] += 1
            if( self.Grid[ row, col ] > self.MAX_PROB ):
                self.Grid[ row, col ] = self.MAX_PROB

    def IncProbCell(self, row, col):
        if( not self.IsWall( row, col ) ):
            self.Grid[ row, col ] += 1
            if( self.Grid[ row, col ] > self.MAX_PROB ):
                self.Grid[ row, col ] = self.MAX_PROB


    def IncProbCells(cells):
        for cell in cells:
            self.IncProbCell( cell[ 0 ], cell[ 1 ] )

    def DecProbCell(self, row, col):
        if( not self.IsWall( row, col ) ):
            self.Grid[ row, col ] -= 1
            if( self.Grid[ row, col ] < self.MIN_PROB ):
                self.Grid[ row, col ] = self.MIN_PROB


    def DecProbCells(cells):
        for cell in cells:
            self.DecProbCell( cell[ 0 ], cell[ 1 ] )


    def DecProb( self, row = int( 0 ), col = int( 0 ) ):
        if( isinstance( row, list ) ):
            for cell in row:
                self.IncProb( cell[ 0 ], cell[ 1 ] )
        elif( not self.IsWall( row, col ) ):
            self.Grid[ row, col ] -= 1
            if( self.Grid[ row, col ] < self.MIN_PROB ):
                self.Grid[ row, col ] = self.MIN_PROB
    
    def CellToPoint( self, r, c ):
        return Point( self.CellWidth * ( c + 0.5 ), self.CellWidth * ( r + 0.5 ) )

    def PointToCell( self, pt ):
        return ( int( pt.y / self.CellWidth ), int( pt.x / self.CellWidth ) )
   
    def IsWall( self, row = 0, col = 0 ):
        return row == 0 or row == self.Rows - 1 or col == 0 or col == self.Cols - 1
