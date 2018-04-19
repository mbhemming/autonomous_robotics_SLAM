function [board_temp_values] = gather_sensor_measurements_for_board(x_robot_EV3UNITS, y_robot_EV3UNITS,      num_sensor_readings_for_a_given_robots_state,     sweep_angle_max,angle_increment,    mysonicsensor,motorRotate,   board ,length_of_side_on_occupency_grid )

%**X&Y cord need to be in EV3 UNITS
%This function will scan the %ultrasonic sensor through a sweep angle = 2*max_sweep_angle gathering data points at each point. 
%The function then returns an temp array that is used for the global board. In this function values of 
%[x_cord,y_cord, radii_of_sensored_object_EV3, dir_robot_DEGREES,
%did_sensor_find_wall] are returned in the temp array. These values can then be used to determined if they should be included in the final board

%% initialized variables

%determines number of sensor increments to make
number_of_discrete_sensor_angles = int32(sweep_angle_max*2/angle_increment);

%zeros the sensor and assumes that it is at parallel to the robot
%direction. At the end of this function the sensor will rezero.
resetRotation(motorRotate);
d_before_sweep = 0;
%Determines current rotation angle (will be zero)
rotation_initial=readRotation(motorRotate);

%% for each angle increment collect sensor data. 

%Add 1 to number_of_discrete_sensor_angles so the last value performs the
%reset of the sensor back to the forwardparallel position 

for j=1:number_of_discrete_sensor_angles+1

    %angle_sweep will if
    %1) j = 1 sweep sensor to max_sweep_angle
    %2) (j<1 j>=number_of_distcrete_sensor_angles) sweep sensor at each
    %increments
    %3) if j = number_of_discrete_sensor_angles + 1 return sensor back to
    %zero position
        
        dir_robot_DEGREES = d_before_sweep + angle_sweep_for_sensor_readings(rotation_initial,sweep_angle_max,angle_increment,motorRotate,number_of_discrete_sensor_angles,   j);
    
        d_before_sweep = dir_robot_DEGREES + d_before_sweep;
        
    % Sensor Data is only collected for
    % j=1:number_of_discrete_sensor_angles
    
    if (j <=number_of_discrete_sensor_angles)
    %% ultrasonic data is now collected and board is drawn for specfic
    %%sensor angle
    
    
        for i=1:num_sensor_readings_for_a_given_robots_state
            sensor_readings(i)=readDistance(mysonicsensor);
        end

        %the mean is now calculated from the sensor measurements
        radii_of_sensored_object_EV3=mean(sensor_readings);

        %test to see if the radii(sensor return) is actually a return from a wall
        did_sensor_find_wall=0; %reset on each loop
        grid_len_in_inches = convert_EV3_units_to_inches( length_of_side_on_occupency_grid )

          
        %See if sensor return is actually a wall not an object of interest
        
        %did_sensor_find_wall= did_sensor_detect_a_wall( x_robot_EV3UNITS, y_robot_EV3UNITS , dir_robot_DEGREES,        radii_of_sensored_object_EV3, tolerance_to_call_distances_the_same,        board, grid_len_in_inches )

        % return 
        %[x cord,   y cord ,  radius of arc,  angle of arc,  did_sensor_find_wall]
             
        %board_temp_values(j,:) = [x_robot_EV3UNITS, y_robot_EV3UNITS, radii_of_sensored_object_EV3, dir_robot_DEGREES, did_sensor_find_wall] ; 
        board_temp_values(j,:) = [radii_of_sensored_object_EV3, dir_robot_DEGREES] ; 
        
    end
    
         
end
 

