import numpy as np
import math

#####################GLOBALS######################
DRIVE_SPEED = 125
SPEED_CONSTANT_CM = 0.007958 # (cm/ms)
SPEED_CONSTANT_IN = 0.00313307086 # (in/ms)

doprint = 0
##################################################

class Driving:
    LENGTH_IN = 12
    WIDTH_IN = 6

    def DriveToPoint( self, dest ):
        # calculate new theta:
        delta_theta = self.CalculateTheta( dest )
        self.TurnTwoWheelDeg( delta_theta )

        #   calculate delta d = sqrt(dX^2 + dY^2)
        #   straight(d)
        self.StraightDistIN( self.CalculateDist( dest ) )
        self.x = dest.x
        self.y = dest.y
        self.Theta += delta_theta

    def TurnOneWheelDeg( self, angle, wheel ):

        # 2.1818 is the ratio of the wheel radius to the robot radius.
        # The formula is the arc length formula. old = 2.1818
        position = 2.22357 * 2 * angle

        if wheel == 'left':
            #turn CW
            self.MRight.stop( stop_action = "hold" )
            self.MLeft.run_to_rel_pos( position_sp = position, \
                                       speed_sp = DRIVE_SPEED, \
                                       stop_action = "hold" )
            self.MLeft.wait_until_not_moving( timeout = 2000 )
        elif wheel == 'right':
            #turn CCW
            self.MLeft.stop( stop_action = "hold" )
            self.MRight.run_to_rel_pos( position_sp = position, \
                                        speed_sp = DRIVE_SPEED, \
                                        stop_action = "hold" )
            self.MRight.wait_until_not_moving( timeout = 2000 )
        else:
            # *Sanity
            print( "invalid wheel", file = sys.error )

    # This function turns the robot to a specified number of degrees using both
    # wheels.
    def TurnTwoWheelDeg( self, angle ):
        # 2.1818 is the ratio of the wheel radius to the robot radius.
        # The formula is the arc length formula. old = 2.1818
        position = 2.22357 *  angle

        # run the motors.
        self.MRight.run_to_rel_pos( position_sp = position, speed_sp = DRIVE_SPEED,\
                                    stop_action = "hold" )
        self.MLeft.run_to_rel_pos( position_sp = -position, speed_sp = DRIVE_SPEED,\
                                   stop_action = "hold" )
        self.MRight.wait_until_not_moving( timeout = 2000 )
        self.MLeft.wait_until_not_moving( timeout = 2000 )

    # Travel straight for a distance measured in CM.
    def StraightDistCM( self, dist ):
        dtMilli =  dist / ( SPEED_CONSTANT_CM )
        self.MLeft.run_to_rel_pos( position_sp = dist * 20.83,\
                                   speed_sp = DRIVE_SPEED, stop_action = "hold" )
        self.MRight.run_to_rel_pos( position_sp = dist * 20.83,\
                                    speed_sp = DRIVE_SPEED, stop_action="hold" )

        self.MLeft.wait_until_not_moving( timeout = dtMilli + 500 )
        self.MRight.wait_until_not_moving( timeout = dtMilli + 500 )
        if( doprint == 1 ):
            print( "Straight:" )
            print( "  dist: " + str( dist ) )
            print( "  dt: " + str( dtMilli ) )

    # Travel straight for a distance measured in IN.
    def StraightDistIN( self, dist ):
        dtMilli =  dist / ( SPEED_CONSTANT_IN )

        self.MLeft.run_to_rel_pos( position_sp = dist * 20.83 * 2.54,\
                                   speed_sp = DRIVE_SPEED, stop_action = "hold" )
        self.MRight.run_to_rel_pos( position_sp = dist * 20.83 * 2.54,\
                                    speed_sp = DRIVE_SPEED, stop_action = "hold" )

        self.MLeft.wait_until_not_moving( timeout = dtMilli + 500 )
        self.MRight.wait_until_not_moving( timeout = dtMilli + 500 )

        if( doprint == 1 ):
            print( "Straight:" )
            print( "  dist: " + str( dist ) )
            print( "  dt: " + str( dtMilli ) )

    def OccupiedCells( self, grid ):
        cen = grid.PointToCell( self.x, self.y )
        len_cells = int( self.LENGTH / ( 2 * grid.CellWidth ) ) + 1
        wid_cells = int( self.WIDTH / ( 2 * grid.CellWidth ) ) + 1
#        bl = ( cen[ 0 ] - 

    def GetCorners( self ):
        thetaRad = math.radians( self.Theta ) 
        half_len = self.LENGTH_IN / 2
        half_wid = self.WIDTH_IN / 2
        cos_theta = math.cos( thetaRad )
        sin_theta = math.sin( thetaRad )
        front = np.array([ half_len * cos_theta + self.x,\
                           half_len * sin_theta + self.y ])
        back = np.array([ -half_len * cos_theta + self.x,\
                          -half_len * sin_theta + self.y ])

        cos_theta = math.cos( thetaRad - math.pi / 2.0 )
        sin_theta = math.sin( thetaRad - math.pi / 2.0 )
       
        fl = np.array([ -half_wid * cos_theta + front[0],\
                        -half_wid * sin_theta + front[1] ])
        bl = np.array([ -half_wid * cos_theta + back[0],\
                        -half_wid * sin_theta + back[1] ])
        fr = np.array([ half_wid * cos_theta + front[0],\
                        half_wid * sin_theta + front[1] ])
        br = np.array([ half_wid * cos_theta + back[0],\
                        half_wid * sin_theta + back[1] ])
        return np.array([ fl, fr, bl, br ])

    # takes in the occupancy grid and the amount of distance (inches) ahead (+) or 
    # behind (-) and checks if the path is clear to move forward or backward
    def PathIsClear( self, grid, dist, debug = False ): 
        thresh = 50
        thetaRad = np.deg2rad( self.Theta )
        botDir = np.array([ np.cos( thetaRad ), np.sin( thetaRad ) ])

        if( dist > 0 ):
            # moving forward, get front corners.
            left, right = self.GetCorners()[ 0:2 ]
            limit = dist + grid.CellWidth
        else:
            # moving backward, get rear corners.
            left, right = self.GetCorners()[ 2:4 ]
            limit = dist - grid.CellWidth

        rowVec = np.subtract( right, left )
        scalars = np.linspace( 0, 1,\
                               2 + self.WIDTH_IN / ( grid.CellWidth * 1.5 ) ) 
        offsets = np.array([ rowVec[0] * scalars, rowVec[1] * scalars ])
        # get next vector,
        end = np.add( left, dist * botDir )
        res = abs( limit / grid.CellWidth )
        pts = np.array([ np.linspace( left[0], end[0], res ),\
                         np.linspace( left[1], end[1], res ) ])
        if( debug ):
            print( "left: " + str( left ) + "\nright: " + str( right ) )
            print( "rowVec: " + str( rowVec ) )
            print( "sc: " + str( scalars ) )
            print( "off: " + str( offsets ) )
            print( "end: " + str( end ) )
            print( "res: " + str( res ) )
            print( "pts: " + str( pts ) )

        for i in range( 1, np.size( pts, 1 ) ):
            points = np.add( offsets,\
                             [ [ pts[0][i] ], [ pts[1][i] ] ] )
            for p in points.T:
                print( ','.join( map( str, p ) ) ) 
            for j in range( np.size( scalars ) ):
                c = grid.PointToCell( points[0][j], points[1][j] )
                if( grid.Grid[ c[0], c[1] ] >= thresh ):
                    return np.linalg.norm( end - left )
        return dist
            








