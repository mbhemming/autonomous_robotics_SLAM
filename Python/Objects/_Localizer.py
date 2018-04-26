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
        prevEndPoint = Point (-1, -1)
        state = 'scanning'
        for angle in range(-180, 180, 2):
            self.SetSensorAngle(float(angle))
            reading = self.SUltra.value()/10.0 #in inches.
            thetaRad = np.deg2rad(angle)
            c = math.cos( thetaRad )
            s = math.sin( thetaRad )
            endPoint = Point( x0 + (reading * c), y0 + (reading * s) )

            print("Angle: " + str(angle) + "Reading: " + str(reading))
            if reading >= 100.3 or not grid.IsWallInches(endPoint.x, endPoint.y):
                state = 'scanning'
            elif state == 'scanning':
                state = 'wall detected'
            elif state == 'wall detected':
                if prevReading > reading:
                    state = 'scanning for minima'
                elif prevReading < reading:
                    state = 'scanning'
            elif state == 'scanning for minima':
                if prevReading < reading:
                    minima = prevReading
                    minAngle = self.Theta + angle - 2
                    print("Minimum distance: " + str(minima))
                    print("at angle: " + str(minAngle))
                                        
                    if prevEndPoint.x < 3 or prevEndPoint.x >  (grid.COURSE_X_IN -3):
                        if prevEndPoint.x > 0.5*grid.COURSE_X_IN:
                            estimatedX = grid.COURSE_X_IN - prevReading
                            estimatedY = prevEndPoint.y
                        else:
                            estimatedX =  prevReading
                            estimatedY = prevEndPoint.y 
                    else:
                        if prevEndPoint.y > 0.5*grid.COURSE_Y_IN:
                            estimatedY = grid.COURSE_Y_IN - prevReading
                            estimatedX = prevEndPoint.x
                        else:
                            estimatedY = prevReading
                            estimatedX = prevEndPoint.x
                            
                    print ("Estimate: " + str((estimatedX,estimatedY)))
                    state = 'scanning'
        
                
            
            prevReading = reading
            prevEndpoint = endPoint
            

        self.ResetSensorAngle()
        #return (minima, prevEndPoint,minAngle)
