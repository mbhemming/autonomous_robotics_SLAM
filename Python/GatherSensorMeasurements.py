import sys
sys.path.insert(0,'./Stats/')
import math
import numpy as np
from ev3Functions import *
from time import sleep
from SonarStatisticsFunctions import DecomposeSensorReadings
def GatherSensorMeasurements(numSensorReadingsForThisState, maxSweepAngleDeg, \
    angleIncrement, sensor, sensorMotor):
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
    numSensorSteps = math.floor(float(maxSweepAngleDeg)*2/float(angleIncrement)) + 1

    angleBeforeSweep = 0
    countReturns = 0
    meanSensorReturns = np.zeros(numSensorSteps+floor(numSensorSteps/2))
    stddevs = np.zeros(numSensorSteps+floor(numSensorSteps/2))
    angles = np.zeros(numSensorSteps+floor(numSensorSteps/2))
    for j in range(0, numSensorSteps):
        # Start the sensor at range the sensor and assumes that it is at 0 degrees relative to the robot.
        angles[countReturns] = maxSweepAngleDeg-(j*angleIncrement)
        SetSensorAngle(sensorMotor, angles[j])
        sensorReadings = np.zeros(numSensorReadingsForThisState)
        sensorMotor.wait_until_not_moving(timeout=1000)
        # Take some number of readings per pointing angle.
        goodReadings = 0
        # if some readings are good and some arent take up to double.
        sanity = numSensorReadingsForThisState
#        sleep(0.1)
        for i in range(0,numSensorReadingsForThisState):
            #sensor.mode = 'US-LISTEN'
            #while( sensor.value() ):
            #    sleep(0.01)
            #sensor.mode = 'US-DIST-IN'
            reading = sensor.value()/10 #in inches.
            
            if reading < 100.3:
                sensorReadings[goodReadings] = reading
                goodReadings = goodReadings + 1
            elif goodReadings > 0 and sanity > 0:
                i = i - 1
                sanity = sanity - 1

        # If we didnt get any 'in range' returns, flag this as inf.
        if goodReadings == 0:
            #meanSensorReturns[j] = np.inf
            #print("Nothing Detected")
            meanSensorReturns[countReturns] = 100.3937007874 # Sensor range max value.
            stddevs[countReturns] = 0.0
            countReturns = countReturns + 1
        else:
            # The mean is now calculated from the valid sensor measurements
            #meanSensorReturns[j] = (np.mean(sensorReadings[0:goodReadings]))
            #stddevs[j] = np.std(sensorReadings[0:goodReadings])
            #print( "Mean: "+ str(np.mean(sensorReadings[0:goodReadings])))
            #print( "StdDev: " + str(np.std(sensorReadings[0:goodReadings])))
            print( str(goodReadings) + " good measurements")
            ranges = DecomposeSensorReadings( sensorReadings[0:goodReadings] , 3)
            for det in ranges:
                print("Detection: " + str(det))
                angles[countReturns] = maxSweepAngleDeg-(j*angleIncrement)
                meanSensorReturns[countReturns] = np.mean(det)
                stddevs[countReturns] = np.std(det)
                countReturns = countReturns + 1
                if meanSensorReturns.size <= countReturns:
                    print("Resizing")
                    meanSensorReturns.resize(countReturns + 10)
                    stddevs.resize(countReturns + 10)
                    angles.resize(countReturns + 10)
    # return sensor to origin.
    ResetSensorAngle(sensorMotor)

    return np.column_stack((angles[0:countReturns],meanSensorReturns[0:countReturns],stddevs[0:countReturns]))
