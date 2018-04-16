function [ out ] = did_sensor_detect_a_wall( x_robot, y_robot, dir_robot,        sensor_measurement, tolerance_to_call_distances_the_same,        board, length_of_grid_square_in_feet )
%DID_SENSOR_DETECT_A WALL Summary of this function goes here
%   Detailed explanation goes here
    
    %get the altitude and angle with respect to that way
    [ altitude, theta_wrt_altitude] = determine_the_altitude_and_theta_to_the_wall( x_robot, y_robot, dir_robot,    board, length_of_grid_square_in_feet );
    
    
    
    %&&&any code to throw out values too close to a corner

    sensor_measurment_predicted = sensor_measurement_prediction_for_wall_return( altitude , theta_wrt_altitude );
    
    if  abs( sensor_measurment_predicted - sensor_measurement) < tolerance_to_call_distances_the_same
       out=1; 
    else
        out=0;
    end
end

