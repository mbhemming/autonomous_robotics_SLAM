
%%%%%%%%%%%%%%%%%%%%%

clear all;

mylego = legoev3('USB');


mysonicsensor = sonicSensor(mylego)


num_readings=100;
sensor_readings=zeros(num_readings,1);
i=1;
while i <= num_readings
    sensor_readings(i)=readDistance(mysonicsensor);
    i=i+1;
end

break_point=1;
