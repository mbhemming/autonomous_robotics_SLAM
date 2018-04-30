function [ distance_to_wall ] = get_distance_to_a_wall( x_EV3,y_EV3,theta_DEGREES, board, length_of_grid_square_in_inches  )
%GET_DISTANCE_TO_A_WALL Summary of this function goes here
%   Detailed explanation goes here
    dir_x_component=cos( to_radians(theta_DEGREES));
    dir_y_component=sin( to_radians(theta_DEGREES));
    [  x_length_of_board_INCHES,y_length_of_board_INCHES  ] = get_board_dims_INCHES( board,length_of_grid_square_in_inches );
    
    if approximately_equal(x_EV3, 1.5494) & approximately_equal(y_EV3, 1.778) & approximately_equal(dir_x_component, -.9848) & approximately_equal(dir_y_component, 0.1736)
       breakpoint=1; 
    end
    
%     if abs(theta_DEGREES-175) <  0.001
%        breakpoint=1; 
%     end
    [ x_out,y_out ] = x_y_of_trejectorys_collision_with_wall(x_EV3,y_EV3,    dir_x_component, dir_y_component,   x_length_of_board_INCHES,y_length_of_board_INCHES  );
    
    distance_to_wall = sqrt (   (x_out-x_EV3)*(x_out-x_EV3)  +   (y_out-y_EV3)*(y_out-y_EV3)   );

end

