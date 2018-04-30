import numpy as np
from Point import Point
import math

class Localizer:
                         
    def TryLocalizing( self, grid):
        startWall = False
        towardMinima = False
        x0 = self.SonarX()
        y0 = self.SonarY()
        prevReading = 100.3+1.0            
        prevEndpoint = Point (-1, -1)
        for angle in range(-180, 180, 2):
            self.SetSensorAngle(float(angle))
            reading = self.SUltra.value()/10.0 #in inches.
            thetaRad = np.deg2rad(angle)
            c = math.cos( thetaRad )
            s = math.sin( thetaRad )
            endPoint = Point( x0 + (reading * c), y0 + (reading * s) )
        
            print("Angle: " + str(angle) + "Reading: " + str(reading))
            if reading < 100.3:
                if grid.IsWallInches(endPoint.x, endPoint.y) == False:
                    startWall = False
                    towardMinima = False
                elif not startWall:
                        startWall = True
                else:
                    if towardMinima == True:
                        if prevReading < reading:
                            print("Closest Wall Point: " + str(prevEndpoint) + " " + str(self.Theta + angle-2.0) + " degrees")
                            startWall = False
                            towardMinima = False
                    elif prevReading > reading:
                        towardMinima = True
                    else: 
                        towardMinima = False
                        startWall = False
        # Kalman Filter if wall minima
                        # if possibly wall:
                        #     Check if Wall:
                        #    startKalman = true/false
                        # if startKalman:
                        #     if prev < this 
                        #        dir = getting further
                        #    else 
                        #        dir = getting closer
                        #    startKalman = false
                        #    kalman started = true
                        # if kalman started
                        #    if dir = getting closer:
                        #        if got farther:
                        #            last was perpandicular. call kalman with angle&dist
                        #            possibly wall = false
                        #    else
                        #        if got closer:
                        #            last was perpandicular to wall call kalman w/angle&d
                        #            possibly wall = false
            else:
                towardMinima = False
                startWall = False
            
            prevReading = reading              
            prevEndpoint = endPoint 
        self.ResetSensorAngle()
