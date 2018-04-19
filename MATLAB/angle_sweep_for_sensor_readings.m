function [current_sensor_angle] = angle_sweep_for_sensor_readings(rotation_initial,sweep_angle_max,angle_increment,motorRotate,number_of_discrete_sensor_angles,   j)


%gear ratio of sensor
gear_ratio = 40/8;

%rotation speed - needs to be greater than 15 so motor doesn't stall
rotate_speed = 20;
motorRotate.Speed = rotate_speed;

%initialize delta_rotation
delta_rotation = 0;


%% Move Sensor
    %Move sensor to furthest angle for sweep
    if (j==1)

        rotate_angle = sweep_angle_max;

        while(abs(delta_rotation) < rotate_angle*gear_ratio)
        rotation = readRotation(motorRotate);
        delta_rotation = abs(rotation - rotation_initial);
        start(motorRotate);    
        end

    end
    
   
    % Now that max angle has been reached begins sweeping through angles by angle increments 
    if (j>1)
    delta_rotation = 0;
    motorRotate.Speed = -rotate_speed;

    rotation_initial_temp = readRotation(motorRotate);

        while (abs(delta_rotation) < angle_increment*gear_ratio)

            rotation = readRotation(motorRotate);
            delta_rotation = abs(rotation - rotation_initial_temp);
            start(motorRotate);    
        end
     
    end
    
    % This step returns the sensor back to the forward (zero'd postion) 
    if (j>number_of_discrete_sensor_angles)
        
         delta_rotation = 0;
         motorRotate.Speed = rotate_speed;
         rotate_angle = sweep_angle_max;
         
                  while (abs(delta_rotation) < rotate_angle*gear_ratio)

                  rotation = readRotation(motorRotate);
                  delta_rotation = abs(rotation - rotation_initial_temp);
                  start(motorRotate);    
                 end
        
    end
    
    stop(motorRotate);
%% Return Back Measurement (if negative need to add 360)
        current_sensor_angle = (readRotation(motorRotate) - rotation_initial)/gear_ratio;
        
        if current_sensor_angle < 0
            current_sensor_angle = 360+current_sensor_angle;
        else
        end
