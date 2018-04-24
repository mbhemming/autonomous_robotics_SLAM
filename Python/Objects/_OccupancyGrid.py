import math
from Robot.Pose import Pose 
from Objects.Point import Point
import numpy as np
class _OccupancyGrid:
    def GetOccupancyUpdate( self, robopose, sonarReturn, sonarRelAngleDeg, dRes=1.5,\
                            angularResDeg=5, sonarFOVDeg=60.0, PRINTSTUFF=True):
    
        roboPose = Pose( robopose )
        sonarCenterAngle = sonarRelAngleDeg + roboPose.Theta
        startAngle = sonarCenterAngle - (sonarFOVDeg/2.0)
    
        x0 = roboPose.x
        y0 = roboPose.y
    
        if PRINTSTUFF:
            print ("robopose: " + str(robopose))
            print ("Sonar Return:  " + str(sonarReturn))
            print ("Sonar Rel: " + str(sonarRelAngleDeg))

        # we will have at most the number of ray angles of plus ones. 
        plusOnes = np.zeros( ( math.floor( sonarFOVDeg / angularResDeg ) + 1, 2 ),\
                   dtype=float)
        nPones = 0
    
        # it's a bit harder to determine how many minus ones, but it is approximately
        # triple.the array can be resized if needed.
        initNumMOnes = math.floor(sonarFOVDeg/angularResDeg)*3
        minOnes = np.zeros((initNumMOnes,2), dtype=float) 
        nMones = 0
    
        for i in range(0, math.floor(sonarFOVDeg/angularResDeg) + 1):
        
            theta =  startAngle + (i*angularResDeg)
            endPoint = Point( x0 + sonarReturn * math.cos( np.deg2rad( theta ) ),\
                              y0 + sonarReturn * math.sin( np.deg2rad( theta ) ) )
        
            endCell =  self.PointToCell( endPoint )
        
            if not any( np.equal( plusOnes, endCell ).all( 1 ) ):
                plusOnes[nPones] = endCell
                nPones = nPones + 1
        print("Plus Ones: " + str( plusOnes[0:nPones]))
        for i in range(0, math.floor( sonarFOVDeg / angularResDeg ) + 1):
            print("i: " + str(i))
            theta =  startAngle + (i*angularResDeg)
            endPoint = Point( x0 + sonarReturn * math.cos( np.deg2rad( theta ) ),\
                              y0 + sonarReturn * math.sin( np.deg2rad( theta ) ) )
        
            # INCHES 
            pointsX = np.linspace( start = x0, stop = endPoint.x,num = int( sonarReturn / dRes ))
            pointsY = np.linspace( start = y0, stop = endPoint.y,num = int( sonarReturn / dRes ) )
        
            for j in range(0, pointsX.size):
#                print("j: " + str(j))
                coord = self.PointToCell( Point( pointsX[ j ],pointsY[ j ] ) )
            
                if (not any( np.equal( plusOnes, coord ).all( 1 ) )) and (not any( np.equal( minOnes, coord ).all( 1 ) )):
                    minOnes[nMones] = coord
                    nMones = nMones + 1
                    if nMones == initNumMOnes:
                        if PRINTSTUFF:
                            print("Resizing Minus Ones to: " + str(2*initNumMOnes))
                        initNumMOnes = initNumMOnes + initNumMOnes
                        minOnes.resize(initNumMOnes)
    
        if PRINTSTUFF:
            print("Plus Ones: " + str( plusOnes[0:nPones]))
            print("Min Ones: " + str( minOnes[0:nMones]))
    
        self.IncProbCells( plusOnes[ 0:nPones ] )
        self.DecProbCells( minOnes[ 0:nMones ] ) 

