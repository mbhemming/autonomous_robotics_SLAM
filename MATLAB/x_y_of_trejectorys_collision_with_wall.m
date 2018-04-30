function [ x_out,y_out ] = x_y_of_trejectorys_collision_with_wall(x_bot_EV3,y_bot_EV3,    dir_x_component, dir_y_component,   x_board_top_corner_INCHES,y_board_top_corner_INCHES  )
%WILL_THE_BOT_COLLIDE_WITH_TOP_OR_BOTTOM Summary of this function goes here
%   Detailed explanation goes here

    if approximately_equal(x_bot_EV3, 1.5494) & approximately_equal(y_bot_EV3, 1.778) & approximately_equal(dir_x_component, -.9848) & approximately_equal(dir_y_component, 0.1736)
       breakpoint=1; 
    end

    x_out=9999;
    y_out=9999;
    
    %get 'm' and 'b' for robots path
    x_next=x_bot_EV3 + dir_x_component;
    y_next=y_bot_EV3 + dir_y_component;
    [ m_robot_path,b_robot_path ] = two_points_to_mx_plus_b(  x_bot_EV3, y_bot_EV3, x_next , y_next  );
    
%     %getting the dimensions that a collision could occur
    [ x_min_search,y_min_search,   x_max_search,y_max_search ] = get_dimensions_a_trejectory_could_hit_wall2( x_bot_EV3,y_bot_EV3,    dir_x_component, dir_y_component,   x_board_top_corner_INCHES,y_board_top_corner_INCHES )
%     
%     intersect_bottom=0;
%     intersect_top=0;
%     intersect_left=0;
%     intersect_right=0;

    x_board_top_corner_EV3=convert_inches_to_EV3_units( x_board_top_corner_INCHES );
    y_board_top_corner_EV3=convert_inches_to_EV3_units( y_board_top_corner_INCHES );

    %test for and intersection with the top
    x_intersect= (y_board_top_corner_EV3-b_robot_path)/m_robot_path;
    if (x_min_search <= x_intersect) & (x_intersect <= x_max_search)
       x_out= x_intersect;
       y_out= y_board_top_corner_EV3;
    end
    
    %test for intersection with the bottom
    x_intersect= (0-b_robot_path)/m_robot_path;
    if (x_min_search <= x_intersect) & (x_intersect <= x_max_search)
       x_out= x_intersect;
       y_out= 0;
    end
    
    %test for intersection with the left
    y_intersect=  b_robot_path;
    if (y_min_search <= y_intersect) & (y_intersect <= y_max_search)
       x_out= 0;
       y_out= y_intersect;
    end
    
    %test for intersection with the right
    y_intersect= m_robot_path * x_board_top_corner_EV3  +   b_robot_path;
    if (y_min_search <= y_intersect) & (y_intersect <= y_max_search)
       x_out= x_board_top_corner_EV3;
       y_out= y_intersect;
    end
    
    if (x_out==9999) | (y_out==9999)
        error('shouldnt occur');
    end
end

