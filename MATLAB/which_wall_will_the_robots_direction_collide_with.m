function [ intersect_left, intersect_right, intersect_bottom, intersect_top ] = which_wall_will_the_robots_direction_collide_with(x_bot,y_bot,    dir_x_component, dir_y_component,   x_board_top_corner_INCHES,y_board_top_corner_INCHES  )
%WILL_THE_BOT_COLLIDE_WITH_TOP_OR_BOTTOM Summary of this function goes here
%   Detailed explanation goes here

    %get 'm' and 'b' for robots path
    x_next=x_bot + dir_x_component;
    y_next=y_bot + dir_y_component;
    [ m_robot_path,b_robot_path ] = two_points_to_mx_plus_b(  x_bot, y_bot, x_next , y_next  );
    
    %getting the dimensions that a collision could occur
    [ x_min_search,y_min_search,   x_max_search,y_max_search ] = get_dimensions_a_trejectory_could_hit_wall2( x_bot,y_bot,    dir_x_component, dir_y_component,   x_board_top_corner_INCHES,y_board_top_corner_INCHES )
    
    intersect_bottom=0;
    intersect_top=0;
    intersect_left=0;
    intersect_right=0;

    x_board_top_corner_EV3=convert_inches_to_EV3_units( x_board_top_corner_INCHES );
    y_board_top_corner_EV3=convert_inches_to_EV3_units( y_board_top_corner_INCHES );

    %test for and intersection with the top
    x_intersect= (y_board_top_corner_EV3-b_robot_path)/m_robot_path;
    if (x_min_search <= x_intersect) & (x_intersect <= x_max_search)
       intersect_top=1; 
    else
        intersect_top=0;
    end
    
    %test for intersection with the bottom
    x_intersect= (0-b_robot_path)/m_robot_path;
    if (x_min_search <= x_intersect) & (x_intersect <= x_max_search)
       intersect_bottom=1; 
    else
        intersect_bottom=0;
    end
    
    %test for intersection with the left
    y_intersect=  b_robot_path;
    if (y_min_search <= y_intersect) & (y_intersect <= y_max_search)
       intersect_left=1; 
    else
        intersect_left=0;
    end
    
    %test for intersection with the right
    y_intersect= m_robot_path * x_board_top_corner_EV3  +   b_robot_path;
    if (y_min_search <= y_intersect) & (y_intersect <= y_max_search)
       intersect_right=1; 
    else
        intersect_right=0;
    end
    
end

