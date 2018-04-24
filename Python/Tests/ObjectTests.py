#!/usr/bin/env python3
import sys
sys.path.append( '../Objects/' )

from Robot.Robot import Robot
from Robot.Pose import Pose
from Point import Point
from OccupancyGrid.OccupancyGrid import OccupancyGrid

TEST_ALL = False
TEST_POINT = False
TEST_POSE = True
TEST_ROBOT = False
TEST_OCC_GRID = False

print( "*********************************" )
print( "*     STARTING OBJECT TESTS     *" )
print( "*********************************" )

# POINT
if( TEST_POINT or TEST_ALL ):
    print( "TESTING POINT" )
    p = Point( 1.2, 1.1 )
    print( p )
    print( str( p.x ) )
    print( str( p.y ) )
    print( "POINT TEST COMPLETE\n\n" )

# POSE
if( TEST_POSE or TEST_ALL ):
    print( "TESTING POSE" )
    print( "Default constructor" )
    ps = Pose( 7.9, 87, 32 )
    print( ps )
    print( "\nList/tuple constructor" )
    t = 3.5, 6.7, 112
    pd = Pose( t )
    print( pd )
    print( "\nCopy constructor" )
    pt = Pose( pd )
    print( pt ) 
    print( "\nPoint-theta constructor" )
    x = Point( 1.2, 1.1 )
    pot = Pose( x, 25 )
    print( pot ) 
    print( "POSE TEST COMPLETE\n\n" )

# OCCUPANCY GRID
if( TEST_OCC_GRID or TEST_ALL ):
    print( "TESTING OCCUPANCY GRID" )
    print( "Default constructor" )
    o = OccupancyGrid( 24, 28, 3 )
    print( "  " + o.Specs() )

    print( "UpdateProb > max" ) 
    o.UpdateProb( 5, 15, 110 )
    print( "  " + str( o.Grid[ 5, 15 ] ) )

    print( "IncProbCell > max" ) 
    o.IncProbCell( 5, 15 )
    print( "  " + str( o.Grid[ 5, 15 ] ) )

    print( "UpdateProb < min" ) 
    o.UpdateProb( 5, 15, -10 )
    print( "  " + str( o.Grid[ 5, 15 ] ) )

    print( "DecProbCell < min" ) 
    o.DecProbCell( 5, 15 )
    print( "  " + str( o.Grid[ 5, 15 ] ) )

    print( "UpdateProb = max" ) 
    o.UpdateProb( 5, 15, 100 )
    print( "  " + str( o.Grid[ 5, 15 ] ) )

    print( "UpdateProb = min" ) 
    o.UpdateProb( 5, 15, 0 )
    print( "  " + str( o.Grid[ 5, 15 ] ) )

    print( "UpdateProb = 34" ) 
    o.UpdateProb( 5, 15, 34 )
    print( "  " + str( o.Grid[ 5, 15 ] ) )

    print( "IncProb" ) 
    o.IncProbCell( 5, 15 )
    print( "  " + str( o.Grid[ 5, 15 ] ) )

    print( "DecProb" ) 
    o.DecProbCell( 5, 15 )
    print( "  " + str( o.Grid[ 5, 15 ] ) )
  
    print( "CellToPoint" )
    p = o.CellToPoint( 15, 12 )
    print( " " + str( p ) )

    print( "PointToCell" )
    c = o.PointToCell( Point( 34.1, 23.2 ) )
    print( " " + str( c ) )


# ROBOT
if( TEST_ROBOT or TEST_ALL ):
    print( "TESTING ROBOT" )
    r = Robot( 10.9, 8.7, 132 )
    print( r )
    print( "DriveToPoint" )
    r.DriveToPoint( Point( 17, 3 ) )
    print( "TurnOneWheelDeg" )
    r.TurnOneWheelDeg( -150, 'right' )
    r.TurnOneWheelDeg( 150, 'left' )
    print( "TurnTwoWheelDeg" )
    r.TurnTwoWheelDeg( 45 )
    print( "StraightDistCM" )
    r.StraightDistCM( -50 )
    print( "StraightDistIN" )
    r.StraightDistIN( 10 )
    print( "CalculateTheta" )
    r.CalculateTheta( Point( 4, 13 ) )
    print( "SetSensorAngle" )
    r.SetSensorAngle( 35 )
    print( "ResetSensorAngle" )
    r.ResetSensorAngle()
    print( "GatherSensorMeasurements" )
    r.GatherSensorMeasurements( 50, 180, 5, o )
    print( "ROBOT TEST COMPLETE\n\n" )


    print( "OCCUPANCY GRID TEST COMPLETE\n\n" )

print( "*********************************" )
print( "*     OBJECT TESTS COMPLETE     *" )
print( "*********************************" )







