function [ altitude, theta_wrt_altitude] = determine_the_altitude_and_theta_to_the_wall( x_robot, y_robot, dir_robot,    board, length_of_grid_square_in_feet )
%GEOMETRICALLY_WHICH_WALL_DO_WE_EXPECT_TO_HIT Summary of this function goes here
%   Detailed explanation goes here
[n_squares_on_y_in_board,n_squares_on_x_in_board] = size(board);
x_length_of_board=n_squares_on_x_in_board*length_of_grid_square_in_feet;
y_length_of_board=n_squares_on_y_in_board*length_of_grid_square_in_feet;

%get second point on robots trejectory
x_on_bots_trejectory=x_robot+3*cos( to_radians(dir_robot) );
y_on_bots_trejectory=y_robot+3*sin( to_radians(dir_robot) );

%reset to not being intersected to re-test for intersection in the code
%below
intersect_bottom=0;
intersect_top=0;
intersect_left=0;
intersect_right=0;


%determine which wall the bot hits & which location%%%%%%%%%%%%%%%%%%%%
intersect_bottom_x_coord=do_lines_intersect_within_a_range(  x_robot, y_robot, x_on_bots_trejectory, y_on_bots_trejectory,    0.001,0.001,x_length_of_board,0.001 );
intersect_top_x_coord=do_lines_intersect_within_a_range(  x_robot, y_robot, x_on_bots_trejectory, y_on_bots_trejectory,    0.001,y_length_of_board,x_length_of_board,y_length_of_board );
intersect_left_x_coord=do_lines_intersect_within_a_range(  x_robot, y_robot, x_on_bots_trejectory, y_on_bots_trejectory,    0.001,0.001,0.001,y_length_of_board );
intersect_right_x_coord=do_lines_intersect_within_a_range(  x_robot, y_robot, x_on_bots_trejectory, y_on_bots_trejectory,    x_length_of_board,0.001,x_length_of_board,y_length_of_board );

if intersect_bottom_x_coord ~= 9999
    intersect_bottom=1;
end
if intersect_top_x_coord ~= 9999
    intersect_top=1;
end
if intersect_left_x_coord ~= 9999
    intersect_left=1;
end
if intersect_right_x_coord ~= 9999
    intersect_right=1;
end

%test
if (intersect_bottom + intersect_top + intersect_left + intersect_right) ~= 1
    error('the robots trejectory must intersect one and only one wall of the enviroment');
end

quad_the_robot_is_aimed = get_quadrant( dir_robot )

%get altitude and angle with respect to altitude
dummy=-9999;
theta_hold=-9999;
altitude=dummy;
delta_y_bots_path=y_on_bots_trejectory - y_robot;
delta_x_bots_path=x_on_bots_trejectory - x_robot;
quad_the_robot_is_aimed = get_quadrant( dir_robot );
if intersect_bottom | intersect_top
    altitude=min(y_robot,y_length_of_board-y_robot);  %this handles both cases of intersect_bottom vs. intersect_top
    
    
    theta_hold = atan_in_degrees_as_magnitude( delta_y_bots_path, delta_x_bots_path )
    theta_wrt_altitude= 90-theta_hold;
    
elseif intersect_right | intersect_left
    altitude=min(x_robot,x_length_of_board-x_robot);
    
    
    theta_hold = atan2_in_degrees_as_magnitude( delta_y_bots_path, delta_x_bots_path )
    theta_wrt_altitude= theta_hold;
    
else
    error('ERROR');
    altitude=dummy;
end

if altitude == dummy
    error('error');
end


end

