function [ output_args ] = did_sensor_detect_a wall( x_robot, y_robot, dir_robot, sensor_measurement,  board )
%DID_SENSOR_DETECT_A WALL Summary of this function goes here
%   Detailed explanation goes here
    
    %get which wall we are taking the reading from
    geometrically_which_wall_do_we_expect_to_hit_with_sensor
    
    %get the altitude and angle with respect to that way
    
    %&&&any code to throw out values too close to a corner

    [ out ] = sensor_measurement_prediction_for_wall_return( altitude , theta )
end

