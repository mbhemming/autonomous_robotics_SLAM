function [ x_min_search,y_min_search,   x_max_search,y_max_search ] = get_dimensions_a_trejectory_could_hit_wall2( x_robot,y_robot,    dir_x_component, dir_y_component,   x_board_top_corner,y_board_top_corner )
%GET_DIMENSIONS_A_TREJECTORY_COULD_HIT_WALL Summary of this function goes here
%   Detailed explanation goes here
% Given the current location and trejectory, there are only certain x and y values
% the the current trejectory could hit the enviorment boundries
    
    x_board_top_corner=convert_inches_to_EV3_units(x_board_top_corner);
    y_board_top_corner=convert_inches_to_EV3_units(y_board_top_corner);

    if dir_x_component > 0
        x_min_search=x_robot;
        x_max_search=x_board_top_corner;
    elseif dir_x_component < 0
        x_min_search=0;
        x_max_search=x_robot;
    else
        x_min_search=x_robot;
        x_max_search=x_robot;
    end
    
    if dir_y_component > 0
        y_min_search=y_robot;
        y_max_search=y_board_top_corner;
    elseif dir_y_component < 0
        y_min_search=0;
        y_max_search=y_robot;
    else
        y_min_search=y_robot;
        y_max_search=y_robot;
    end

    
end

