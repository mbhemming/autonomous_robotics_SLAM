import sys
sys.path.insert(0,'../')

import ev3dev.ev3 as ev3
import ev3Functions as ev3f
from RobotPose import RobotPose

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
        delta_theta = ev3f.CalculateTheta( dest, self.Pose )
        ev3f.TurnTwoWheelDeg( delta_theta, self.MLeft, self.MRight )

        #   calculate delta d = sqrt(dX^2 + dY^2)
        #   straight(d)
        ev3f.StraightDistIN( ev3f.CalculateDist( dest, self.Pose.Pt ),\
                             self.MLeft, self.MRight )
        self.Pose.Pt.x = dest.x
        self.Pose.Pt.y = dest.y
        self.Pose.Theta += delta_theta

        # This function turns the robot to a specified angle using only 1 wheel.
        # This does not look at color values while turning.
        def TurnOneWheelDeg( angle, motorLeft, motorRight, wheel ):

        # 2.1818 is the ratio of the wheel radius to the robot radius.
        # The formula is the arc length formula.
        position = 2.1818 * 2 * angle

        if wheel == 'left':
            #turn CW
            motorRight.stop( stop_action = "hold" )
            motorLeft.run_to_rel_pos( position_sp = position, \
                                  speed_sp = DRIVE_SPEED, \
                                  stop_action = "hold" )
        elif wheel == 'right':
            #turn CCW
            motorLeft.stop( stop_action = "hold" )
            motorRight.run_to_rel_pos( position_sp = position, \
                                   speed_sp = DRIVE_SPEED, \
                                   stop_action = "hold" )
        else:
            # *Sanity
            print( "invalid wheel", file = sys.error )


