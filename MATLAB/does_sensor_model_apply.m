function [ out ] = does_sensor_model_apply(  x_robot, y_robot,dir_robot, board, length_of_grid_square_in_feet )
%DOES_SENSOR_MODEL_APPLY Summary of this function goes here
%   Detailed explanation goes here

    %get the altitude and angle with respect to that way
    [ altitude_EV3, theta_wrt_altitude] = determine_the_altitude_and_theta_to_the_wall( x_robot, y_robot, ...
        dir_robot, board, length_of_grid_square_in_feet );
    altitude_FEET = convert_EV3_units_to_inches( altitude_EV3 ) / 12;

    %get interpolated value to see if its 99. This means the sensor model
    %diddn't apply
    [ interpolated_value ] = sensor_measurement_prediction_for_wall_return( altitude_FEET , theta_wrt_altitude )
    
    if interpolated_value == 99
        out=0;
    else
        out=1;
    end

end

