#!/usr/bin/env python3
import sys
sys.path.append('./Objects' )
from Robot import Robot
from Point import Point
from OccupancyGrid import OccupancyGrid

##################INITIALIZATION##################

bot = Robot( 61.125, -4.5, 90 )
occGrid = OccupancyGrid( 3 )

##################################################
StartCell = occGrid.PointToCell( Point( 61.125, 6 ) ) 
FirstWaypoint = occGrid.CellToPoint( StartCell[ 0 ], StartCell[ 1 ] )

bot.DriveToPoint( FirstWaypoint ) 
