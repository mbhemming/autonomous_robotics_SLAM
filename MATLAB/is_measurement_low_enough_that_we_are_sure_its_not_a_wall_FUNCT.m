function [ out ] = is_measurement_low_enough_that_we_are_sure_its_not_a_wall_FUNCT(  x_EV3, y_EV3 , dir_DEGREES,        radii_of_sensored_object_EV3,        board, grid_len_in_inches )  
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

    %get the minimum distance a wall could be based on the sensors cone
    [ distance_to_wall_CCW_EDGE_OF_CONE ] = get_distance_to_a_wall( x_EV3, y_EV3, dir_DEGREES-30, board, grid_len_in_inches );
    [ distance_to_wall_DIRECTION_OF_BOT ] = get_distance_to_a_wall( x_EV3, y_EV3, dir_DEGREES, board, grid_len_in_inches );
    [ distance_to_wall_CW_EDGE_OF_CONE ] = get_distance_to_a_wall( x_EV3, y_EV3, dir_DEGREES+30, board, grid_len_in_inches );
    min_distance_we_expect_a_wall_to_be = min( [ distance_to_wall_CCW_EDGE_OF_CONE distance_to_wall_DIRECTION_OF_BOT distance_to_wall_CW_EDGE_OF_CONE ] );
            
     %error catching
     catch_error_vector_size( min_distance_we_expect_a_wall_to_be,1,1 )
    
    %output
    if radii_of_sensored_object_EV3 < 0.75 * min_distance_we_expect_a_wall_to_be
       out = 1; 
    else
        out = 0;
    end


end

