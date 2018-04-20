%method: A protractor was used to draw lines on the floor...

clear all;

mylego = legoev3('USB');

mysonicsensor = sonicSensor(mylego);

%set up for each moving of the box
true_distance_the_object_is_away=1.1871;


num_readings=100;
sensor_readings=zeros(num_readings,1);
tolerance=.5;  %how close the measurment must be to be a hit
num_time_the_object_was_successfully_detected=0;
i=1;
for i=1:num_readings
    sensor_readings(i)=readDistance(mysonicsensor);
    if(  abs(sensor_readings(i)-true_distance_the_object_is_away) <  tolerance )
        num_time_the_object_was_successfully_detected=num_time_the_object_was_successfully_detected+1;
    end
end

%looking for an 80% detection rate to say the object has been located
num_time_the_object_was_successfully_detected/num_readings
%mean(sensor_readings)


