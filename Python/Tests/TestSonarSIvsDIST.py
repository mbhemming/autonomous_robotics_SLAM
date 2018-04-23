#!/usr/bin/env python3
import sys
sys.path.append( '../Objects/Robot' )
sys.path.append( '../Objects' )
from Robot import Robot

##################INITIALIZATION##################
#start = RobotPose( Point( 0, 0 ), 90 )

bot = Robot( 0, 0, 90 )
print( bot )
##################################################

print( "Continuous " + bot.SUltra.mode )
for i in range( 0, 1000 ):
    bot.SUltra.mode = 'US-DIST-IN'
    print( bot.SUltra.value() )
    bot.SUltra.mode = 'US-LISTEN'
    if( bot.SUltra.value() ):
        print( "!!!!!!!!!!" )
