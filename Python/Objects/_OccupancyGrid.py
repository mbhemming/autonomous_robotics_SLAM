import math
from Point import Point
from Pose import Pose 
import numpy as np
class _OccupancyGrid:
    def GetOccupancyUpdate( self, robopose, sonarReturn, sonarRelAngleDeg, dRes=0.25,\
        angularResDeg=2.0, raySide = 0, sonarFOVDeg=40.0, angleStep = 0.0,  PRINTSTUFF=False):
    
        roboPose = Pose( robopose )
        sonarCenterAngle = sonarRelAngleDeg + roboPose.Theta

        # If we only need to do the right side
        sonarFOVDeg = sonarFOVDeg - 2.0*angleStep
        startAngle = sonarCenterAngle - (sonarFOVDeg/2.0)
        if raySide == 1:
            startAngle = sonarCenterAngle - (sonarFOVDeg/2.0) - (angleStep)
            sonarFOVDeg = angleStep
        elif raySide == -1:
            startAngle = startAngle + sonarFOVDeg/2.0
            sonarFOVDeg = angleStep
            

        lastcoord=(-1,-1) 
        x0 = roboPose.x
        y0 = roboPose.y
    
        if PRINTSTUFF:
            print ("robopose: " + str(robopose))
            print ("Sonar Return:  " + str(sonarReturn))
            print ("Sonar Rel: " + str(sonarRelAngleDeg))
            print ("Direction: " + str(raySide))
            print ("FOV: " + str(sonarFOVDeg))
            print ("Start Angle: " + str(startAngle))

        # we will have at most the number of ray angles of plus ones. 
        plusOnes = np.zeros( ( math.floor( sonarFOVDeg / angularResDeg ) + 1, 2 ),\
                   dtype=float)
        nPones = 0
    
        # it's a bit harder to determine how many minus ones, but it is approximately
        # triple.the array can be resized if needed.
        initNumMOnes = (plusOnes.shape[0]) *10
        minOnes = np.zeros((initNumMOnes,2), dtype=float) 
        nMones = 0
        if sonarReturn <= 36: 
            for i in range(0, math.floor(sonarFOVDeg/angularResDeg) + 1):
                thetaRad = np.deg2rad( startAngle + (i*angularResDeg))
                endPoint = Point( x0 + sonarReturn * math.cos( thetaRad ),\
                                  y0 + sonarReturn * math.sin( thetaRad ) )
        
                endCell =  self.PointToCell( endPoint )
                
                # Don't smear from walls. if any point was a wall point, ignore this return.
                #if self.IsWall(endCell[0],endCell[1]):
                #    plusOnes = np.zeros( ( math.floor( sonarFOVDeg / angularResDeg ) + 1, 2 ),\
                #    dtype=float)
                #    nPones = 0
                #    break
                    
                    
                if not any( np.equal( plusOnes, endCell ).all( 1 ) ):
                    plusOnes[nPones] = endCell
                    nPones = nPones + 1
        else:
            sonarReturn = 36 # Still lower some cells.
        if sonarReturn > 6:    
            for i in range(0, math.floor( sonarFOVDeg / angularResDeg ) + 1):
                thetaRad =  np.deg2rad(startAngle + (i*angularResDeg))
                startX = x0+5*math.cos( thetaRad)
                startY = y0+5*math.sin(thetaRad)
                endPoint = Point( x0 + sonarReturn * math.cos( thetaRad ),\
                                  y0 + sonarReturn * math.sin( thetaRad ) )
        
                # INCHES ** Potential Performance: generate the points once and move them ** 
                pointsX = np.linspace( start = startX, stop = endPoint.x,num = \
                                                                  int( (sonarReturn-6 )/ dRes ))
                pointsY = np.linspace( start = startY, stop = endPoint.y,num = \
                                                                  int( (sonarReturn-6) / dRes ) )
        
                for j in range(0, pointsX.size):
                    if pointsX[j] < 0 or pointsY [ j ] < 0:
                        break

                    coord = self.PointToCell( Point( pointsX[ j ],pointsY[ j ] ) )
                    lastcoord = coord
                    if coord != lastcoord and (self.Grid[coord[0], coord[1]] != 0) and (not self.IsWall(coord[0],coord[1])):
            
                        if (not any( np.equal( plusOnes, coord ).all( 1 ) )) and (not any( np.equal( minOnes, coord ).all( 1 ) )):
                            minOnes[nMones] = coord
                            nMones = nMones + 1
                            if nMones == minOnes.shape[0]:
                                #initNumMOnes = initNumMOnes + initNumMOnes
                                z = np.zeros((initNumMOnes,2), dtype=float)
                                print("Before resize: " + str(minOnes))
                                minOnes = np.concatenate((minOnes,z), axis=0)
                                print("After: " + str(minOnes))
                                print("Resizing Minus Ones: " + str(minOnes.shape[0]))
    
        if PRINTSTUFF:
            print("Plus Ones: " + str( plusOnes[0:nPones]))
            print("Min Ones: " + str( minOnes[0:nMones]))
    
        self.IncProbCells( plusOnes[ 0:nPones ] )
        self.DecProbCells( minOnes[ 0:nMones ] ) 

        
        
    def GetOccupancyUpdate2( self, robopose, sonarReturn, sonarRelAngleDeg, dRes=0.15,\
        angularResDeg=10.0, raySide = 0, sonarFOVDeg=60.0, angleStep = 0.0,  PRINTSTUFF=False):
    
        roboPose = Pose( robopose )
        sonarCenterAngle = sonarRelAngleDeg + roboPose.Theta

        # If we only need to do the right side
        startAngle = sonarCenterAngle - (sonarFOVDeg/2.0)
        stopAngle = startAngle + sonarFOVDeg
        if raySide == 1:
            stopAngle = startAngle + angleStep 
        elif raySide == -1:
            startAngle = sonarCenterAngle + sonarFOVDeg/2.0
            stopAngle = startAngle + angleStep
            
        coveredDegrees = stopAngle - startAngle
        numberRays = ( math.floor( coveredDegrees / angularResDeg ) + 1 )
        
        lastcoord=(-1,-1) 
        x0 = roboPose.x
        y0 = roboPose.y
        
        if PRINTSTUFF:
            print("StartAngle: " + str(startAngle))
            print("StopAngle: " + str(stopAngle))

        # we will have at most the number of ray angles of plus ones. 
        plusOnes = np.zeros( (numberRays, 2 ), dtype=float)
        nPones = 0
    
        # it's a bit harder to determine how many minus ones, but it is approximately
        # triple.the array can be resized if needed.
        initNumMOnes = numberRays *10
        minOnes = np.zeros((initNumMOnes,2), dtype=float) 
        nMones = 0
        
        if sonarReturn <= 24: 
            for i in range(0, numberRays):
                thetaRad = np.deg2rad( startAngle + (i*angularResDeg))
                endPoint = Point( x0 + sonarReturn * math.cos( thetaRad ),\
                                  y0 + sonarReturn * math.sin( thetaRad ) )
        
                endCell =  self.PointToCell( endPoint )
                
                # Don't smear from walls. if any point was a wall point, ignore this return.
                if self.IsWall(endCell[0],endCell[1]):
                    plusOnes = np.zeros( ( math.floor( sonarFOVDeg / angularResDeg ) + 1, 2 ),\
                    dtype=float)
                    nPones = 0
                    break
                    
                    
                if not any( np.equal( plusOnes, endCell ).all( 1 ) ):
                    plusOnes[nPones] = endCell
                    nPones = nPones + 1
        else:
            sonarReturn = 24 # Still lower some cells.
            
            
        if sonarReturn > 4:    
            for i in range(0, numberRays):
                thetaRad =  np.deg2rad(startAngle + (i*angularResDeg))
                startX = x0+2*math.cos( thetaRad)
                startY = y0+2*math.sin(thetaRad)
                endPoint = Point( x0 + sonarReturn * math.cos( thetaRad ),\
                                  y0 + sonarReturn * math.sin( thetaRad ) )
        
                # INCHES ** Potential Performance: generate the points once and move them ** 
                pointsX = np.linspace( start = startX, stop = endPoint.x,num = \
                                                                  int( (sonarReturn-6 )/ dRes ))
                pointsY = np.linspace( start = startY, stop = endPoint.y,num = \
                                                                  int( (sonarReturn-6) / dRes ) )
        
                for j in range(0, pointsX.size):
                    if pointsX[j] < 0 or pointsY [ j ] < 0:
                        break

                    coord = self.PointToCell( Point( pointsX[ j ],pointsY[ j ] ) )
                    lastcoord = coord
                    if coord != lastcoord and (self.Grid[coord[0], coord[1]] != 0):
            
                        if (not any( np.equal( plusOnes, coord ).all( 1 ) )) and (not any( np.equal( minOnes, coord ).all( 1 ) )):
                            minOnes[nMones] = coord
                            nMones = nMones + 1
                            if nMones == minOnes.shape[0]:
                                #initNumMOnes = initNumMOnes + initNumMOnes
                                z = np.zeros((initNumMOnes,2), dtype=float)
                                print("Before resize: " + str(minOnes))
                                minOnes = np.concatenate((minOnes,z), axis=0)
                                print("After: " + str(minOnes))
                                print("Resizing Minus Ones: " + str(minOnes.shape[0]))
    
        if PRINTSTUFF:
            print("Plus Ones: " + str( plusOnes[0:nPones]))
            print("Min Ones: " + str( minOnes[0:nMones]))
    
        self.IncProbCells( plusOnes[ 0:nPones ] )
        self.DecProbCells( minOnes[ 0:nMones ] ) 
