import numpy as np
import math
import time

#####################GLOBALS######################
DRIVE_SPEED = 150
SPEED_CONSTANT_CM = 0.007958 # (cm/ms)
SPEED_CONSTANT_IN = 0.003 # (in/ms)
#TICKS_PER_INCH = 20.83 * 2.54
TICKS_PER_INCH = 52.8627977995

doprint = 0
##################################################

class Driving:
    LENGTH_IN = 12
    WIDTH_IN = 6

    def DriveToPoint( self, dest, grid, force = False ):
        # calculate new theta:
        delta_theta = self.CalculateTheta( dest )
        if( not force and ( abs(delta_theta) > 45 and not self.TurnIsClear( grid ) ) ):
            print ("Couldnt Turn.")
            return 1 # couldn't turn

        self.TurnTwoWheelDeg( delta_theta )

        #   calculate delta d = sqrt(dX^2 + dY^2)
        #   straight(d)
        dist = np.linalg.norm( [self.x - dest.x, self.y-dest.y] )
        if( not force and\
            ( abs(self.PathIsClear( grid, dist, self.Theta ) ) < abs(dist) ) ):
            print("Path Not Clear") 
            return 2 # path not clear

        return self.StraightDistIN( dist, grid )

    def TurnOneWheelDeg( self, angle, wheel ):
        assert False
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
        self.Theta += angle

    # Travel straight for a distance measured in IN.
    def StraightDistIN( self, dist, grid ):
        dtMilli =  math.fabs( dist / SPEED_CONSTANT_IN )

        self.MLeft.reset()
        self.MRight.reset()
        print( "go straight: " + str( dist ) )
        self.MLeft.run_to_rel_pos( position_sp = dist * TICKS_PER_INCH,\
                                   speed_sp = DRIVE_SPEED, stop_action = "hold" )
        self.MRight.run_to_rel_pos( position_sp = dist * TICKS_PER_INCH,\
                                    speed_sp = DRIVE_SPEED, stop_action = "hold" )

        st = round(time.time()*1000)

        while( ( self.MLeft.is_running or self.MRight.is_running ) and\
               ( not ( round(time.time()*1000) - st > dtMilli ) ) ):

            if( dist > 0 and self.STouch.value() ):
                self.MLeft.stop()
                self.MRight.stop()
                print( "bumped!!" )
                delta = ( self.MLeft.position + self.MLeft.position )\
                        / ( 2 * TICKS_PER_INCH )
                self.x += delta * np.cos( np.rad2deg( self.Theta ) )
                self.y += delta * np.sin( np.rad2deg( self.Theta ) )
                # Update grid cells to indicate presence of object
                left, right = self.GetCorners()[ 0:2 ]
                rowVec = np.subtract( right, left )
                scalars = np.linspace( 0, 1,\
                               2 + self.WIDTH_IN / ( grid.CellWidth * 1.5 ) ) 
                offsets = np.array([ rowVec[0] * scalars, rowVec[1] * scalars ])
                points = np.add( offsets,\
                             [ [ left[0] ], [ left[1] ] ] )
                for j in range( np.size( scalars ) ):
                    c = grid.PointToCell( points[0][j], points[1][j] )
                    grid.Grid[ c ] = 100

                self.StraightDistIN( -self.LENGTH_IN/2, grid )
                
                return 3 # bumped into something and backe up

        # sanity
        self.MLeft.stop()
        self.MRight.stop()
        
        delta = ( self.MLeft.position + self.MRight.position ) / ( 2 * TICKS_PER_INCH )
        self.x += delta * np.cos( np.deg2rad( self.Theta ) )
        self.y += delta * np.sin( np.deg2rad( self.Theta ) )
        return 0 # made it to waypoint

    # Returns the row and column of bottom left and top right cells to 
    # indicate the rectangle of occupied cells. The return type is a 2x2 numpy array
    def OccupiedCells( self, grid ):
        corners = self.GetCorners( 'cells', grid )
#        for c in corners:
#            print( ','.join( map( str, c ) ) ) 
#        print( type(corners ))
        rmin = np.min( corners[:,0] )
        rmax = np.max( corners[:,0] )
        cmin = np.min( corners[:,1] )
        cmax = np.max( corners[:,1] )
        
        return np.array( [ [ rmin, cmin ], [ rmax, cmax ] ] )

    def GetCorners( self, tp = 'points', grid = [] ):
        thetaRad = math.radians( self.Theta ) 
        half_len = self.LENGTH_IN / 2
        half_wid = self.WIDTH_IN / 2
        cos_theta = math.cos( thetaRad )
        sin_theta = math.sin( thetaRad )
        front = np.array([ half_len * cos_theta + self.x,\
                           half_len * sin_theta + self.y ])
        back = np.array([ -half_len * cos_theta + self.x,\
                          -half_len * sin_theta + self.y ])

        xy = np.array([ math.cos( thetaRad - math.pi / 2.0 ),\
                        math.sin( thetaRad - math.pi / 2.0 ) ])
       
        fl = np.add( -half_wid * xy, front )
        bl = np.add( -half_wid * xy, back )
        fr = np.add( half_wid * xy, front )
        br = np.add( half_wid * xy, back )
        pts = [ fl, fr, bl, br ]

#        for p in pts:
#            print( ','.join( map( str, p ) ) ) 
       
        if( tp == 'points' ):
            return pts
        elif( tp == 'cells' ):
            return np.array([ grid.PointToCell( n[0], n[1] ) for n in pts ])
        else:
            return []

    # takes in the occupancy grid and the amount of distance (inches) ahead (+) or 
    # behind (-) and checks if the path is clear to move forward or backward
    def PathIsClear( self, grid, dist, theta, thresh = 35, debug = False ): 
        print( "checking path: " )
        thetaRad = np.deg2rad( theta )
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
        end = np.add( left, limit * botDir )
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
#            for p in points.T:
#                print( ','.join( map( str, p ) ) ) 
            for j in range( np.size( scalars ) ):
                c = grid.PointToCell( points[0][j], points[1][j] )
#                print( "cell: " + str( c ) ) 
#                print( "val: " + str( grid.Grid[ c ] ) )
                if( grid.Grid[ c ] >= thresh ):
                    return np.sign( dist ) *\
                           np.linalg.norm( left - [ pts[0][i], pts[1][i] ] )
        
        return dist
            
    def TurnIsClear( self, grid ):
        thresh = 25
        radius = np.linalg.norm( [self.WIDTH_IN/2, self.LENGTH_IN/2] )
        bl = np.subtract([ self.x, self.y ], radius )
        tr = np.add([ self.x, self.y ], radius )
        cells = np.array([grid.PointToCell( p[0], p[1] ) for p in [ bl, tr ] ])
        return grid.CheckCells( cells )






