#!/usr/bin/env python3
import sys
sys.path.append( '../Objects' )
sys.path.append( '../Objects/Robot' )
sys.path.append( '../Objects/OccupancyGrid' )

from Robot.Robot import Robot
from Point import Point
from Pose import Pose
from OccupancyGrid import OccupancyGrid

TEST_ALL = False
TEST_POINT = False
TEST_POSE = False
TEST_ROBOT = False
TEST_OCC_GRID = True

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
    print( "List/tuple constructor" )
    t = 3.5, 6.7, 112
    pd = Pose( t )
    print( pd )
    print( "Copy constructor" )
    pt = Pose( pd )
    print( pt ) 
    print( "Point-theta constructor" )
    pt = Pose( Point( 1.2, 1.1 ), 25 )
    print( pt ) 
    print( "POSE TEST COMPLETE\n\n" )

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
    r.GatherSensorMeasurements( 50, 180, 5 )
    print( "ROBOT TEST COMPLETE\n\n" )

# OCCUPANCY GRID
if( TEST_OCC_GRID or TEST_ALL ):
    print( "TESTING OCCUPANCY GRID" )
    print( "Default constructor" )
    o = OccupancyGrid( 24, 28, 3 )
    print( "  " + o.Specs() )

    print( "UpdateProb > max" ) 
    o.UpdateProb( 5, 15, 110 )
    print( "  " + str( o.Grid[ 5, 15 ] ) )

    print( "IncProb > max" ) 
    o.IncProb( 5, 15 )
    print( "  " + str( o.Grid[ 5, 15 ] ) )

    print( "UpdateProb < min" ) 
    o.UpdateProb( 5, 15, -10 )
    print( "  " + str( o.Grid[ 5, 15 ] ) )

    print( "DecProb < min" ) 
    o.DecProb( 5, 15 )
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
    o.IncProb( 5, 15 )
    print( "  " + str( o.Grid[ 5, 15 ] ) )

    print( "DecProb" ) 
    o.DecProb( 5, 15 )
    print( "  " + str( o.Grid[ 5, 15 ] ) )
  
    print( "CellToPoint" )
    p = o.CellToPoint( 15, 12 )
    print( " " + str( p ) )

    print( "PointToCell" )
    c = o.PointToCell( Point( 34.1, 23.2 ) )
    print( " " + str( c ) )


    print( "OCCUPANCY GRID TEST COMPLETE\n\n" )

print( "*********************************" )
print( "*     OBJECT TESTS COMPLETE     *" )
print( "*********************************" )







