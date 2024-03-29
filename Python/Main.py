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

bot = Robot( 61.1, -5.5, 90 )
occGrid = OccupancyGrid( 1 )

#waypoints = [ Point( 61.1, 34.9 ),\
 #             Point( 61.1, 53.75 ),\
  #            Point( 16, 53.75 ),\
   #           Point( 16, 34.9 ),\
    #          Point( 16, 16 ),\
     #         Point( 61.1, 16 ) ] 
waypoints = [ Point( 61.1, 53.75 ),\
              Point( 16, 53.75 ),\
              Point( 16, 16 ),\
              Point( 61.1, 16 ) ] 

##################################################

e.Sound.beep()
while not button.any():
    sleep( 0.01 )

sleep( 5 )

bot.StraightDistIN( 16 + 5.5, occGrid )
data = bot.GatherSensorMeasurements2( 30, 180, 5, occGrid )
printer.AppendToCsv( csvfile, bot, data )
#occGrid.DECR_AMOUNT = 24
#occGrid.INCR_AMOUNT = 15
for p in waypoints:
    manovers = 0
    backups = 0
    while( math.hypot( p.x-bot.x, p.y-bot.y ) > 6 ):
        res = bot.DriveToPoint( p, occGrid ) 
        print( bot )
        print( res )
        if( res == 1 ):
            print( "couldn't turn" )             
            # couldn't turn, reverse
            bot.StraightDistIN( -6, occGrid )
            backups = backups + 1
            # force turn.
            #bot.TurnTwoWheelDeg( bot.CalculateTheta( p ) )
            res = 2
            
        if( res == 2 ):
            print( "path not clear" )             
            multiplier = 1
            t = bot.Theta + multiplier * 15
            odd = True
            while( bot.PathIsClear( occGrid, 16, t ) < 16 ):
#                print( "m: " + str( multiplier ) )
 #               print( "o: " + str( odd ) )
                if( odd ):
                    multiplier = -multiplier
                else:
                    multiplier = -multiplier + 1
                odd = not odd
                if( abs( multiplier ) > 6 ):
                    break
                t = bot.Theta + multiplier * 15
            
            if( abs( multiplier ) > 6 ):
                bot.DriveToPoint( p, occGrid, True )
            else:
                bot.TurnTwoWheelDeg( multiplier * 15 )
                bot.StraightDistIN( 16, occGrid )

            manovers += 1
            if manovers > 4:
                occGrid = OccupancyGrid(1)
                bot.GatherSensorMeasurements2( 30, 180, 5, occGrid)
                
            # path not clear or bumped something.    

    data = bot.GatherSensorMeasurements2( 30, 180, 5, occGrid )
    printer.GridToCsv( occGrid , '_DEMO_')
    printer.AppendToCsv( csvfile, bot, data )

bot.TurnTwoWheelDeg( bot.CalculateTheta( Point (61.1, 0)) )
bot.StraightDistIN( 30, occGrid )

