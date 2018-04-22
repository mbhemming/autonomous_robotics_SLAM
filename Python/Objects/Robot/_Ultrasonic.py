#####################GLOBALS######################
GEAR_RATIO = 40/8
ROTATION_SPEED = 200
##################################################i

class Ultrasonic:

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

