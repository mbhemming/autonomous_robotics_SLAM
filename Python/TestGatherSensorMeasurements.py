import numpy as np
from GatherSensorMeasurements import GatherSensorMeasurements
from ev3dev.ev3 import *

us = UltrasonicSensor()
assert us.connected, "Connect US"

us.mode = 'US-DIST-IN'

sm = MediumMotor()
assert sm.connected, "motor not connected"

print(np.array(GatherSensorMeasurements(50,45,3,us,sm)))


