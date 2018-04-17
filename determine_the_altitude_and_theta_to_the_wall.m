function [ altitude, theta_wrt_altitude] = determine_the_altitude_and_theta_to_the_wall( x_robot_EV3, y_robot_EV3, dir_robot,    board, length_of_grid_square_in_inches )
%GEOMETRICALLY_WHICH_WALL_DO_WE_EXPECT_TO_HIT Summary of this function goes here
%   Detailed explanation goes here
[n_squares_on_y_in_board,n_squares_on_x_in_board] = size(board);
x_length_of_board_EV3=n_squares_on_x_in_board*convert_inches_to_EV3_units(length_of_grid_square_in_inches);
y_length_of_board_EV3=n_squares_on_y_in_board*convert_inches_to_EV3_units(length_of_grid_square_in_inches);
x_length_of_board_INCHES=n_squares_on_x_in_board*length_of_grid_square_in_inches;
y_length_of_board_INCHES=n_squares_on_y_in_board*length_of_grid_square_in_inches;

%get second point on robots trejectory
x_on_bots_trejectory=x_robot_EV3+3*cos( to_radians(dir_robot) );
y_on_bots_trejectory=y_robot_EV3+3*sin( to_radians(dir_robot) );

%reset to not being intersected to re-test for intersection in the code
%below
intersect_bottom=0;
intersect_top=0;
intersect_left=0;
intersect_right=0;


%determine which wall the bot hits & which location%%%%%%%%%%%%%%%%%%%%
dir_x_component=x_on_bots_trejectory-x_robot_EV3;
dir_y_component=y_on_bots_trejectory-y_robot_EV3;

[ intersect_left, intersect_right, intersect_bottom, intersect_top ] = which_wall_will_the_robots_direction_collide_with(x_robot_EV3,y_robot_EV3,    dir_x_component, dir_y_component,   x_length_of_board_INCHES,y_length_of_board_INCHES  )


%test
if (intersect_bottom + intersect_top + intersect_left + intersect_right) ~= 1
    error('the robots trejectory must intersect one and only one wall of the enviroment');
end

quad_the_robot_is_aimed = get_quadrant( dir_robot )

%get altitude and angle with respect to altitude
dummy=-9999;
theta_hold=-9999;
altitude=dummy;
delta_y_bots_path=y_on_bots_trejectory - y_robot_EV3;
delta_x_bots_path=x_on_bots_trejectory - x_robot_EV3;
quad_the_robot_is_aimed = get_quadrant( dir_robot );
if intersect_bottom | intersect_top
    altitude=min(y_robot_EV3,y_length_of_board_EV3-y_robot_EV3);  %this handles both cases of intersect_bottom vs. intersect_top
    
    
    theta_hold = atan_in_degrees_as_magnitude( delta_y_bots_path, delta_x_bots_path )
    theta_wrt_altitude= 90-theta_hold;
    
elseif intersect_right | intersect_left
    altitude=min(x_robot_EV3,x_length_of_board_EV3-x_robot_EV3);
    
    
    theta_hold = atan_in_degrees_as_magnitude( delta_y_bots_path, delta_x_bots_path )
    theta_wrt_altitude= theta_hold;
    
else
    error('ERROR');
    altitude=dummy;
end

if altitude == dummy
    error('error');
end


end

