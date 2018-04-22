import sys
sys.path.insert(0,'../')

import ev3dev.ev3 as ev3
import ev3Functions as ev3f
from RobotPose import RobotPose

######################ENUMS#######################
class ROTATION(Enum):
    CW = 1
    CCW = 2
##################################################

#####################GLOBALS######################
GEAR_RATIO = 40/8
ROTATION_SPEED = 200

DRIVE_SPEED = 125
SPEED_CONSTANT_CM = 0.007958 # (cm/ms) 
SPEED_CONSTANT_IN = 0.00313307086 # (in/ms) 
##################################################

class Robot:
        
    def __init__( self, pose ):
        self.Pose = pose
        self.MLeft = ev3.LargeMotor('outD')
        self.MRight = ev3.LargeMotor('outA')
        self.MUltra = ev3.MediumMotor()
        self.SUltra = ev3.UltrasonicSensor()
        self.STouch = ev3.TouchSensor()

        assert self.MLeft.connected, "Left motor not connected"
        assert self.MRight.connected, "Right motor not connected" 
        assert self.MUltra.connected, "Ultrasonic (medium) motor not connected"
        assert self.SUltra.connected, "Ultrasonic sensor not connected"
        assert self.STouch.connected, "Touch sensor not connected"
        
        # Stop all motors for sanity
        self.MRight.stop()
        self.MLeft.stop()
        self.MUltra.stop()

        # Change ultrasonic sensor mode to continuous inches.
        # US-DIST-IN range is 0-1003 (1003 is 255 cm)
        self.SUltra.mode = 'US-DIST-IN'
        
        # Zero the ultrasonic sensor angle
        ev3f.ResetSensorAngle( self.MUltra )
    
    def __str__( self ):
        return str( self.Pose )
 
    def DriveToPoint( self, dest ):
        # calculate new theta:
        delta_theta = self.CalculateTheta( dest )
        self.TurnTwoWheelDeg( delta_theta )

        #   calculate delta d = sqrt(dX^2 + dY^2)
        #   straight(d)
        self.StraightDistIN( self.CalculateDist( dest ) )
        self.Pose.Pt.x = dest.x
        self.Pose.Pt.y = dest.y
        self.Pose.Theta += delta_theta

        # This function turns the robot to a specified angle using only 1 wheel.
        # This does not look at color values while turning.
        def TurnOneWheelDeg( self, angle, wheel ):

            # 2.1818 is the ratio of the wheel radius to the robot radius.
            # The formula is the arc length formula.
            position = 2.1818 * 2 * angle

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
                                    speed_sp = DRIVE_SPEED,\ stop_action="hold" )

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

    # Calculate angle between current robot angle and desired position
    # Arguments:
    #     dest: destination point as Point object
    #     pose: robot pose as Pose object
    # Returns:
    #     angle between pose.Theta and vector created from pose.Pt and dest
    def CalculateTheta( self, dest ):
        # formula found on math stack exchange
        # calc current unit vector of robot using current theta
        x1 = math.cos( math.radians( slef.Pose.Theta ) ) 
        y1 = math.sin( math.radians( slef.Pose.Theta ) )

        # calc vector to travel along.
        x2 = dest.x - slef.Pose.Pt.x
        y2 = dest.y - slef.Pose.Pt.y 
        
        dot = x1 * x2 + y1 * y2      # dot product
        det = x1 * y2 - y1 * x2      # determinant 

        # atan2(y, x) or atan2(sin, cos )
        return math.degrees( math.atan2( det, dot ) ) 

    # Set the sensor angle to a theta relative to the forward facing position.
    def SetSensorAngle( self, angle ):
        self.MUltra.wait_until_not_moving( timeout = 1000 )
        self.MUltra.run_to_abs_pos( position_sp = angle * GEAR_RATIO,\
                                    speed_sp = ROTATION_SPEED )

    # Return sensor to forward facing position and reset position_sp variable
    def ResetSensorAngle( self ):
        self.MUltra.wait_until_not_moving( timeout = 1000 )
        self.MUltra.run_to_abs_pos( position_sp = 0, speed_sp = ROTATION_SPEED )
        self.MUltra.position_sp = 0
        return 0        
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        