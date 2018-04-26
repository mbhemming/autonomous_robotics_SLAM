import math
import numpy as np
#from OccupancyGrid import OccupancyGrid
from Pose import Pose
#####################GLOBALS######################
GEAR_RATIO = 40/8
ROTATION_SPEED = 200
STALL_TIME_CONSTANT = 0.03
##################################################i

class Ultrasonic:

    # Set the sensor angle to a theta relative to the forward facing position.
    def SetSensorAngle( self, angle ):
        tim = math.fabs( angle - self.MUltra.position / GEAR_RATIO )\
                         / STALL_TIME_CONSTANT
        self.MUltra.run_to_abs_pos( position_sp = angle * GEAR_RATIO,\
                                     speed_sp = ROTATION_SPEED )
        self.MUltra.wait_until_not_moving( timeout = tim )

    # Return sensor to forward facing position and reset position_sp variable
    def ResetSensorAngle( self ):
        tim = math.fabs( self.MUltra.position / GEAR_RATIO ) / STALL_TIME_CONSTANT
        self.MUltra.run_to_abs_pos( position_sp = 0, speed_sp = ROTATION_SPEED )
        self.MUltra.wait_until_not_moving( timeout = tim )

    def DecomposeSensorReadings( self, allReadings, granularity ):

        sortedReadings = np.sort( allReadings )
        #print(sortedReadings)

        bins =[]

        category = 0
        start = 0
        i = 0
        while i < sortedReadings.size:
            category = sortedReadings[i]
            #print("Category: " + str(category))
            while i<sortedReadings.size and sortedReadings[i]-category < granularity:
                i = i + 1
            if start != i:
                #print(sortedReadings[start:i])
                bins.append(sortedReadings[start:i])
                start = i
            i = i + 1

        #print(bins)
        return bins

    def GatherSensorMeasurements( self, numSensorReadingsForThisState,\
                                  maxSweepAngleDeg, angleIncrement , grid):
        """
        ** X&Y cord need to be in fine resolution map co-ordinates.
        This function will scan the ultrasonic sensor through a sweep angle\
        = 2*max_sweep_angle gathering data points at each point. 
        The function then returns an temp array that is used for the global board.\
        In this function values of 
        [sonarAngleDegrees ,  meanSensorReturns] this is a table of two columns.
    
        """
        self.ScanCount += 1

        if angleIncrement < 3:
            angleIncrement = 3

        # determines number of sensor increments to make
        numSensorSteps = math.floor( float( maxSweepAngleDeg ) * 2\
                                     / float( angleIncrement ) ) + 1

        angleBeforeSweep = 0
        countReturns = 0
        side = 0 #center
        detectionRange = 60.0 #deg
        meanSensorReturns = np.zeros(numSensorSteps+math.floor(numSensorSteps/2))
        stddevs = np.zeros(numSensorSteps+math.floor(numSensorSteps/2))
        angles = np.zeros(numSensorSteps+math.floor(numSensorSteps/2))
        prevReturn = -1
        for j in range(0, numSensorSteps):
            # Start the sensor at range the sensor and assumes that it is at 0 
            # degrees relative to the robot.
            angles[countReturns] = maxSweepAngleDeg-(j*angleIncrement)
            #self.SetSensorAngle( angles[j] )
            self.SetSensorAngle( maxSweepAngleDeg-(j*angleIncrement) )
            sensorReadings = np.zeros(numSensorReadingsForThisState)
            self.MUltra.wait_until_not_moving(timeout=1000)
            # Take some number of readings per pointing angle.
            goodReadings = 0
            # if some readings are good and some arent take up to double.
            sanity = numSensorReadingsForThisState
            for i in range(0,numSensorReadingsForThisState):
                reading = self.SUltra.value()/10 #in inches.
                
                if reading < 100.3:
                    sensorReadings[goodReadings] = reading
                    goodReadings = goodReadings + 1
                elif goodReadings > 0 and sanity > 0:
                    i = i - 1
                    sanity = sanity - 1

            # If we didnt get any 'in range' returns, flag this as inf.
            if goodReadings == 0:
                # Sensor range max value.
                meanSensorReturns[countReturns] = 100.3937007874
                #stddevs[countReturns] = 0.0
                countReturns = countReturns + 1
            else:
                # The mean is now calculated from the valid sensor measurements
                ranges = self.DecomposeSensorReadings( sensorReadings[0:goodReadings], 3)
                for det in ranges:
                    #print("Detection: " + str(det))
                    angles[countReturns] = maxSweepAngleDeg-(j*angleIncrement)
                    meanSensorReturns[countReturns] = np.mean(det)
                    if prevReturn < 0:
                        side = 0
                        #detectionRange = 0.0
                    elif (prevReturn - meanSensorReturns[countReturns])>12.0:
                        print("Found an object CW at: " + str(angles[countReturns]))
                        #detectionRange = angleIncrement
                        side = 1
                    elif (prevReturn - meanSensorReturns[countReturns])<-12.0:
                        print("Left an object CW at: " + str(angles[countReturns]))
                        #detectionRange = angleIncrement
                        side = -1
                    else: 
                        #detectionRange = 0.0
                        side = 0

                    prevReturn = meanSensorReturns[countReturns]

                    grid.GetOccupancyUpdate2(Pose(self.x,self.y,self.Theta), meanSensorReturns[countReturns],maxSweepAngleDeg-(j*angleIncrement), raySide = side, sonarFOVDeg = 60.0, angleStep = angleIncrement, PRINTSTUFF=True)
#                    print("Finished Range: " + str(meanSensorReturns[countReturns]))
                    #stddevs[countReturns] = np.std(det)
                    countReturns = countReturns + 1
                    if meanSensorReturns.size <= countReturns:
                        #print("Resizing")
                        meanSensorReturns.resize(countReturns + 10)
                        #stddevs.resize(countReturns + 10)
                        angles.resize(countReturns + 10)


        # return sensor to origin.
        self.ResetSensorAngle()
        
        return np.column_stack( ( angles[ 0:countReturns ],\
                                  meanSensorReturns[ 0:countReturns ],\
                                  stddevs[ 0:countReturns ] ) )
                                      
    def GatherSensorMeasurements2( self, numSensorReadingsForThisState,\
                                  maxSweepAngleDeg, angleIncrement , grid):
        """
        ** X&Y cord need to be in fine resolution map co-ordinates.
        This function will scan the ultrasonic sensor through a sweep angle\
        = 2*max_sweep_angle gathering data points at each point. 
        The function then returns an temp array that is used for the global board.\
        In this function values of 
        [sonarAngleDegrees ,  meanSensorReturns] this is a table of two columns.
    
        """

        if angleIncrement < 3:
            angleIncrement = 3

        # determines number of sensor increments to make
        numSensorSteps = math.floor( float( maxSweepAngleDeg ) \
                                     / float( angleIncrement ) ) + 1

        angleBeforeSweep = 0
        countReturns = 0
        side = 0 #center
        detectionRange = 60.0 #deg
        meanSensorReturns = np.zeros(numSensorSteps+math.floor(numSensorSteps/2))
        stddevs = np.zeros(numSensorSteps+math.floor(numSensorSteps/2))
        angles = np.zeros(numSensorSteps+math.floor(numSensorSteps/2))
        
        prevReturn = -1
        currAngle = 0.0
        signs = (1,-1)
        for k in range(0,1):
            signDir = signs[k]
            for i in range(0,1):
                signAng = signs[i]
                for j in range(0, numSensorSteps):
                    # Start the sensor at range the sensor and assumes that it is at 0 
                    # degrees relative to the robot.
                    nextAngle = currAngle + signDir*signAng*(j*angleIncrement)
                    angles[countReturns] = nextAngle
                    #self.SetSensorAngle( angles[j] )
                    self.SetSensorAngle( nextAngle ) 
                    
                    sensorReadings = np.zeros(numSensorReadingsForThisState)
                    # Take some number of readings per pointing angle.
                    goodReadings = 0
                    # if some readings are good and some arent take up to double.
                    sanity = numSensorReadingsForThisState
                    for i in range(0,numSensorReadingsForThisState):
                        reading = self.SUltra.value()/10 #in inches.
                        
                        if reading < 100.3:
                            sensorReadings[goodReadings] = reading
                            goodReadings = goodReadings + 1
                        elif goodReadings > 0 and sanity > 0:
                            i = i - 1
                            sanity = sanity - 1

                    # If we didnt get any 'in range' returns, flag this as inf.
                    if goodReadings == 0:
                        # Sensor range max value.
                        meanSensorReturns[countReturns] = 100.3937007874
                        #stddevs[countReturns] = 0.0
                        countReturns = countReturns + 1
                    else:
                        # The mean is now calculated from the valid sensor measurements
                        ranges = self.DecomposeSensorReadings( sensorReadings[0:goodReadings], 3)
                        for det in ranges:
                            #print("Detection: " + str(det))
                            angles[countReturns] = nextAngle
                            meanSensorReturns[countReturns] = np.mean(det)
                            if prevReturn < 0:
                                side = 0
                                #detectionRange = 0.0
                            elif (prevReturn - meanSensorReturns[countReturns])>12.0:
                                print("Found an object CW at: " + str(angles[countReturns]))
                                #detectionRange = angleIncrement
                                side = 1
                            elif (prevReturn - meanSensorReturns[countReturns])<-12.0:
                                print("Left an object CW at: " + str(angles[countReturns]))
                                #detectionRange = angleIncrement
                                side = -1
                            else: 
                                #detectionRange = 0.0
                                side = 0

                            prevReturn = meanSensorReturns[countReturns]

                            grid.GetOccupancyUpdate(Pose(self.x,self.y,self.Theta), meanSensorReturns[countReturns], nextAngle, raySide = signDir*signAng*side, sonarFOVDeg = 60.0, angleStep = angleIncrement)

                            countReturns = countReturns + 1
                            if meanSensorReturns.size <= countReturns:
                                #print("Resizing")
                                meanSensorReturns.resize(countReturns + 10)
                                #stddevs.resize(countReturns + 10)
                                angles.resize(countReturns + 10)


        
        return np.column_stack( ( angles[ 0:countReturns ],\
                                  meanSensorReturns[ 0:countReturns ],\
                                  stddevs[ 0:countReturns ] ) )
