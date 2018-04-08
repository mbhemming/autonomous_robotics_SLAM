
%%%%%%%%%%%%%%%%%%%%%

clear all;

mylego = legoev3('USB');
%myev3 = legoev3('Bluetooth','/dev/tty.EV3-SerialPort');
% 
% motorRight = motor(mylego,'A');
% motorLeft = motor(mylego,'B');
% 
% motorRight.Speed=10;
% motorLeft.Speed=10;

mysonicsensor = sonicSensor(mylego)

%corrective_factor_between_sensor_readings_and_ft=

num_readings=1000;
sensor_readings=zeros(num_readings,1);
i=1;
while i <= num_readings
    sensor_readings(i)=readDistance(mysonicsensor);
    i=i+1;
end

plot(sensor_readings);
title('test1 - ultra-sonic sensor readings for the sensor at 4 foot from a wall')
xlabel('iteration number') % x-axis label
ylabel('sensor reading') % y-axis label


%linear regression
[slope, y_intercept]=polyfit(1:num_readings,sensor_readings',1)
