function [ altitude, theta_wrt_altitude] = geometrically_which_wall_do_we_expect_to_hit_with_sensor( x_robot, y_robot, dir_robot,    board, length_of_grid_square_in_meters )
%GEOMETRICALLY_WHICH_WALL_DO_WE_EXPECT_TO_HIT Summary of this function goes here
%   Detailed explanation goes here
[n_squares_on_y_in_board,n_squares_on_x_in_board] = size(board);
x_length_of_board=n_squares_on_x_in_board*length_of_grid_square_in_meters;
y_length_of_board=n_squares_on_y_in_board*length_of_grid_square_in_meters;

%get second point on robots trejectory
x_on_bots_trejectory=x_robot+3*cos( to_radians(dir) );
y_on_bots_trejectory=y_robot+3*sin( to_radians(dir) );

%determine which wall the bot hits & which location%%%%%%%%%%%%%%%%%%%%
intersect_bottom=do_lines_intersect_within_a_range(  x_robot, y_robot, x_on_bots_trejectory, y_on_bots_trejectory,    0.001,0.001,x_length_of_board,0.001 );
intersect_top=do_lines_intersect_within_a_range(  x_robot, y_robot, x_on_bots_trejectory, y_on_bots_trejectory,    0.001,y_length_of_board,x_length_of_board,y_length_of_board );
intersect_left=do_lines_intersect_within_a_range(  x_robot, y_robot, x_on_bots_trejectory, y_on_bots_trejectory,    0.001,0.001,0.001,y_length_of_board );
intersect_right=do_lines_intersect_within_a_range(  x_robot, y_robot, x_on_bots_trejectory, y_on_bots_trejectory,    x_length_of_board,0.001,x_length_of_board,y_length_of_board );

%test
if (intersect_bottom + intersect_top + intersect_left + intersect_right) ~= 1
    error('the robots trejectory must intersect one and only one wall of the enviroment');
end

quad_the_robot_is_aimed = get_quadrant( dir )

%get altitude and angle
dummy=-9999;
theta_hold=dummy;
delta_y_bots_path=y_on_bots_trejectory - y_robot;
delta_x_bots_path=x_on_bots_trejectory - x_robot;
quad_the_robot_is_aimed = get_quadrant( dir );
if intersect_bottom | intersect_top
    altitude=y_robot;
    
    if (quad_the_robot_is_aimed == 3) | (quad_the_robot_is_aimed == 4)
        theta_hold = atan2_in_degrees_as_magnitude( delta_y_bots_path, delta_x_bots_path )
        theta_wrt_altitude= 90-theta_hold;
    else
        error('this quadrant should not occur');
    end
elseif intersect_right | intersect_left
    
    if (quad_the_robot_is_aimed == 1) | (quad_the_robot_is_aimed == 2)
        theta_hold = atan2_in_degrees_as_magnitude( delta_y_bots_path, delta_x_bots_path )
        theta_wrt_altitude= theta_hold;
    else
        error('this quadrant should not occur');
    end
else
    error('ERROR');
end




end

