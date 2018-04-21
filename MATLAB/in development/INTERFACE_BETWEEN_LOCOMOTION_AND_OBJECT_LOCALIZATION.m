function [ board ] = INTERFACE_BETWEEN_LOCOMOTION_AND_OBJECT_LOCALIZATION( x_robot_EV3UNITS, y_robot_EV3UNITS , dir_sensor_DEGREES,    board,grid_len_in_inches  mysonicsensor,motorRotate )
%INTERFACE_BETWEEN_LOCOMOTION_AND_OBJECT_LOCALIZATION Summary of this function goes here
%   Detailed explanation goes here

%setup filtering params
ignore_walls=1;
min_radius_to_draw_at=1.2;


%setup other
num_sensor_readings_for_a_given_robots_state=100;
arc_theta=60;
sweep_angle_max=90;     %**********this will likely need to get changed
angle_increment=2;
thickness_of_arc_to_draw=4;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%   Gather enviroment info - potential arcs to draw
[range_and_theta_pairs] = gather_sensor_measurements_for_board(x_robot_EV3UNITS, y_robot_EV3UNITS,      num_sensor_readings_for_a_given_robots_state,     sweep_angle_max,angle_increment,    mysonicsensor,motorRotate,   board,grid_len_in_inches   ,length_of_side_on_occupency_grid );
[n dummy]=size(range_and_theta_pairs);

%   Update board with arcs that suggest object locations
for i=1:n
    
    radii_of_sensored_object_EV3=range_and_theta_pairs(i,1);
    dir_sensor_DEGREES=range_and_theta_pairs(i,2);
    
     
    %if the sensed object(or possibly wall) is too far, then we won't draw
    is_sensor_model_applicable= does_sensor_model_apply(  x_robot_EV3, y_robot_EV3,dir_sensor_DEGREES, board, length_of_grid_square_in_feet )
    if radii_of_sensored_object_EV3 < min_radius_to_draw_at
        if ignore_walls ==1
            if is_sensor_model_applicable==1
                did_sensor_find_wall=did_sensor_detect_a_wall( x_robot_EV3UNITS, y_robot_EV3UNITS , dir_sensor_DEGREES,        radii_of_sensored_object_EV3, tolerance_to_call_distances_the_same,        board, grid_len_in_inches )
                if  (did_sensor_find_wall == 0)
                    board=get_circular_arc_for_drawing( x_robot_EV3UNITS, y_robot_EV3UNITS , dir_sensor_DEGREES,       radii_of_sensored_object_EV3, arc_theta, thickness_of_arc_to_draw,     board,grid_len_in_inches );
                end
            else %if the sensor model isn't applicable then we use a heuristic to get the minimum distance we expect a wall to be
                is_measurement_low_enough_that_we_are_sure_its_not_a_wall=is_measurement_low_enough_that_we_are_sure_its_not_a_wall_FUNCT(  x_robot_EV3UNITS, y_robot_EV3UNITS , dir_sensor_DEGREES,        radii_of_sensored_object_EV3,        board, grid_len_in_inches ) ;
                if is_measurement_low_enough_that_we_are_sure_its_not_a_wall ==1
                    board=get_circular_arc_for_drawing( x_robot_EV3UNITS, y_robot_EV3UNITS , dir_sensor_DEGREES,       radius_EV3, arc_theta, thickness_of_arc_to_draw,     board,grid_len_in_inches );
                end
            end
        elseif ignore_wall==0 %if we arn't ignoring the walls then just draw
            board=get_circular_arc_for_drawing( x_robot_EV3UNITS, y_robot_EV3UNITS , dir_sensor_DEGREES,       radius_EV3, arc_theta, thickness_of_arc_to_draw,     board,grid_len_in_inches );
        end
        
        
    end
end

end

