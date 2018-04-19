function [current_sensor_angle] = angle_sweep(rotation_initial,sweep_angle_max,angle_increment,j,motorRotate,number_of_discrete_sensor_angles)



%gear ratio of sensor
gear_ratio = 40/8;
rotate_speed = 20;


motorRotate.Speed = rotate_speed;
delta_rotation = 0;

%Move sensor to furthest angle for sweep
if (j==1)
    rotate_angle = sweep_angle_max;
    
    while(abs(delta_rotation) < rotate_angle*gear_ratio);
    rotation = readRotation(motorRotate);
    delta_rotation = abs(rotation - rotation_initial);
    start(motorRotate);    
    end
    
end
    
stop(motorRotate)

if (j>1)
delta_rotation = 0;
motorRotate.Speed = -rotate_speed;

rotation_initial_temp = readRotation(motorRotate);

while (abs(delta_rotation) < angle_increment*gear_ratio)
    
    rotation = readRotation(motorRotate);
    delta_rotation = abs(rotation - rotation_initial_temp);
    start(motorRotate);    
end

stop(motorRotate) 
end
    

current_sensor_angle = (readRotation(motorRotate) - rotation_initial)/gear_ratio;
if current_sensor_angle < 0
    current_sensor_angle = 360+current_sensor_angle;
else
end
end