import math
from Point import Point
from Pose import Pose 
import numpy as np
class _OccupancyGrid:
    def GetOccupancyUpdate( self, robopose, sonarReturn, sonarRelAngleDeg, dRes=1.5,\
                            angularResDeg=6, sonarFOVDeg=60.0, PRINTSTUFF=False):
    
        roboPose = Pose( robopose )
        sonarCenterAngle = sonarRelAngleDeg + roboPose.Theta
        startAngle = sonarCenterAngle - (sonarFOVDeg/2.0)
           lastcoord=(-1,-1) 
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
        initNumMOnes = math.floor(sonarFOVDeg/angularResDeg)*5
        minOnes = np.zeros((initNumMOnes,2), dtype=float) 
        nMones = 0
        if sonarReturn <= 24: 
            for i in range(0, math.floor(sonarFOVDeg/angularResDeg) + 1):
                theta =  startAngle + (i*angularResDeg)
                endPoint = Point( x0 + sonarReturn * math.cos( np.deg2rad( theta ) ),\
                                  y0 + sonarReturn * math.sin( np.deg2rad( theta ) ) )
        
                endCell =  self.PointToCell( endPoint )
        
                if not any( np.equal( plusOnes, endCell ).all( 1 ) ):
                    plusOnes[nPones] = endCell
                    nPones = nPones + 1
        else:
            sonarReturn = 24 # Still lower some cells.
        if sonarReturn > 6:    
            for i in range(0, math.floor( sonarFOVDeg / angularResDeg ) + 1):
                theta =  startAngle + (i*angularResDeg)
                startX = x0+5*math.cos( np.deg2rad( theta ))
                startY = y0+5*math.sin(np.deg2rad( theta ))
                endPoint = Point( x0 + sonarReturn * math.cos( np.deg2rad( theta ) ),\
                                  y0 + sonarReturn * math.sin( np.deg2rad( theta ) ) )
        
                # INCHES 
                pointsX = np.linspace( start = startX, stop = endPoint.x,num = int( (sonarReturn-6 )/ dRes ))
                pointsY = np.linspace( start = startY, stop = endPoint.y,num = int( (sonarReturn-6) / dRes ) )
        
                for j in range(0, pointsX.size):
                    coord = self.PointToCell( Point( pointsX[ j ],pointsY[ j ] ) )
                    if coord != lastcoord:
                        lastcoord=coord            
                        if (not any( np.equal( plusOnes, coord ).all( 1 ) )) and (not any( np.equal( minOnes, coord ).all( 1 ) )):
                            minOnes[nMones] = coord
                            nMones = nMones + 1
                            if nMones == initNumMOnes:
                                if PRINTSTUFF:
                                    print("Resizing Minus Ones to: " + str(2*initNumMOnes))
                                initNumMOnes = initNumMOnes + initNumMOnes
                                minOnes.reshape(initNumMOnes,2)
    
        if PRINTSTUFF:
            print("Plus Ones: " + str( plusOnes[0:nPones]))
            print("Min Ones: " + str( minOnes[0:nMones]))
    
        self.IncProbCells( plusOnes[ 0:nPones ] )
        self.DecProbCells( minOnes[ 0:nMones ] ) 
