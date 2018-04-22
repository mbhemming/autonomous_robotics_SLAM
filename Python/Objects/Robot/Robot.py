import sys
sys.path.append('../')

import ev3dev.ev3 as ev3
import math
from Pose import Pose
from _Driving import Driving
from _Ultrasonic import Ultrasonic

#####################GLOBALS######################
GEAR_RATIO = 40/8
ROTATION_SPEED = 200
##################################################

class Robot( Pose, Driving, Ultrasonic ):
        
    def __init__( self, x, y, theta ):
        Pose.__init__( self, x, y, theta )
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
        self.ResetSensorAngle()
    
    def __str__( self ):
        return Pose.__str__( self )
 
    # Calculate angle between current robot angle and desired position
    # Arguments:
    #     dest: destination point as Point object
    #     pose: robot pose as Pose object
    # Returns:
    #     angle between pose.Theta and vector created from pose.Pt and dest
    def CalculateTheta( self, dest ):
        # formula found on math stack exchange
        # calc current unit vector of robot using current theta
        x1 = math.cos( math.radians( self.Theta ) ) 
        y1 = math.sin( math.radians( self.Theta ) )

        # calc vector to travel along.
        x2 = dest.x - self.x
        y2 = dest.y - self.y 
        
        dot = x1 * x2 + y1 * y2      # dot product
        det = x1 * y2 - y1 * x2      # determinant 

        # atan2(y, x) or atan2(sin, cos )
        return math.degrees( math.atan2( det, dot ) ) 

    # Calculate the euclidean distance between pose.Pt and dest
    def CalculateDist( self, dst ): 
        dx = self.x - dst.x
        dy = self.y - dst.y
        return math.hypot( dx, dy )

                   
        
        
        
