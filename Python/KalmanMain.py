#!/usr/bin/env python3
import sys
sys.path.append('./Objects' )
sys.path.append('./Functions' )
import ev3dev.ev3 as e
from Robot import Robot
from Point import Point
from OccupancyGrid import OccupancyGrid
from time import sleep
import FileOutputter as printer 
import math

##################INITIALIZATION##################

button = e.Button()

csvfile = open( 'rawSonarData.csv', 'w' )

bot = Robot( 64.0, 14, 90 )
occGrid = OccupancyGrid( 1 )

waypoints = [ Point( 61.1, 23.5 ), Point( 61.1, 25.0 ) ] 

##################################################

e.Sound.beep()
#while not button.any():
#    sleep( 0.01 )

sleep( 5 )

#bot.StraightDistIN( 20.5, occGrid )
#data = bot.GatherSensorMeasurements2( 30, 180, 5, occGrid )
#bot.TryLocalizing(occGrid)
#printer.AppendToCsv( csvfile, bot, data )

for p in waypoints:
    while( math.hypot( p.x-bot.x, p.y-bot.y ) > 6 ):
#        res = bot.DriveToPoint( p, occGrid ) 
        sleep(2) 
       #print( bot )
        #print( res )
        #if( res == 1 ):
        #    # couldn't turn, reverse
        #    bot.StraightDistIN( -6, occGrid )
        #    continue
        #elif( res == 2 ):
        #    print( "path not clear" )             
        #    multiplier = 1
        #    t = bot.Theta + multiplier * 15
        #    odd = True
        #    while( bot.PathIsClear( occGrid, 16, t ) < 12 ):
        #        print( "m: " + str( multiplier ) )
        #        print( "o: " + str( odd ) )
        #        if( odd ):
        #            multiplier = -multiplier
        #        else:
        #            multiplier = -multiplier + 1
        #        odd = not odd
        #        if( abs( multiplier ) > 6 ):
        #            break
        #        t = bot.Theta + multiplier * 15
        #    
        #    if( abs( multiplier ) > 6 ):
        #        bot.DriveToPoint( p, occGrid, True )
         #   else:
         #       bot.TurnTwoWheelDeg( multiplier * 15 )
         #       bot.StraightDistIN( 12, occGrid )

            
            # path not clear or bumped something.    
        #data = bot.GatherSensorMeasurements2( 30, 180, 5, occGrid )
        bot.TryLocalizing(occGrid)

#bot.TurnTwoWheelDeg( bot.CalculateTheta( Point (61.1, 0)) )
#bot.StraightDistIN( 30, occGrid )

