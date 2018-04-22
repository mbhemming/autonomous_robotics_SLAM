import ev3dev.ev3 as ev3
from Pose import Pose
import math

#####################GLOBALS######################
DRIVE_SPEED = 125
SPEED_CONSTANT_CM = 0.007958 # (cm/ms)
SPEED_CONSTANT_IN = 0.00313307086 # (in/ms)

doprint = 0
##################################################

class Driving:
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
        elif wheel == 'right':
            #turn CCW
            self.MLeft.stop( stop_action = "hold" )
            self.MRight.run_to_rel_pos( position_sp = position, \
                                        speed_sp = DRIVE_SPEED, \
                                        stop_action = "hold" )
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


