clear all;

mylego = legoev3('USB');
%myev3 = legoev3('Bluetooth','/dev/tty.EV3-SerialPort');

motorRight = motor(mylego,'A');
motorLeft = motor(mylego,'B');

mysonicsensor = sonicSensor(mylego)


motorRight.Speed=10;
motorLeft.Speed=10;



reset_rotation_both_motors(motorLeft,motorRight );


%corrective_factor_between_sensor_readings_and_ft=


%NOTE: This must come after reseting wheel rotation
start(motorLeft);
start(motorRight);
