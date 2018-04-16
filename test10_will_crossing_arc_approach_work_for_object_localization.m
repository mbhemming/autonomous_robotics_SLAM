
clear all;

mylego = legoev3('USB');

mysonicsensor = sonicSensor(mylego);

%set up%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


num_sensor_readings_for_a_given_robots_state=100;
tolerance_for_grouping_distance_as_the_same=.5;  %how close the measurment must be to be a hit
thickness_of_arc_to_draw=4;  %seems logical
arc_theta=60;  %the total sweep of the cone

length_of_side_on_occupency_grid=convert_inches_to_EV3_units(0.25);
length_of_enviroment=convert_inches_to_EV3_units(69.25);     %***these are in the robots units. We can make them in inches later
width_of_enviroment=convert_inches_to_EV3_units(80.25);

tolerance_to_call_distances_the_same=convert_inches_to_EV3_units(6);  

%%%%%%***ad the sensor's position in relation to the robots centre
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
board=zeros(    int32(length_of_enviroment/length_of_side_on_occupency_grid)    );

dummy_value=9999;
robot_state_x_y_direction=[dummy_value dummy_value dummy_value];  %initializing this variable but it will be over-written

sensor_readings=zeros(num_sensor_readings_for_a_given_robots_state,1);
i=1;

 x=12*1;
 y=42.5;
d=180;

while 1==1
    
    %break_point=dummy_value;  %set breakpoint here and manually type in the robots state
    breakpoint=1;
    x_robot=convert_inches_to_EV3_units( x );
    y_robot=convert_inches_to_EV3_units( y );
    dir_robot=d;
    
    %make sure the vector is still 1x3
    %catch_error_vector_size( robot_state_x_y_direction,1,3 )
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%either get senosr measuments or load a
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%% vector of previously recorded sensor
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%% measuremnts
    %get n sensor readings 
    for i=1:num_sensor_readings_for_a_given_robots_state
        sensor_readings(i)=readDistance(mysonicsensor);
    end
    %load('sensor_readings.mat');
    
    %%%****log the number of times we get more than one radius
    
    %Get the radii for the arcs
    radii_of_sensored_object=get_radii_of_prospective_objects( sensor_readings );
    %radii_of_sensored_object=convert_inches_to_EV3_units( x ) + .5;
    
    %test to see if the radii(sensor return) is actually a return from a
    %wall
    did_sensor_find_wall=0; %reset on each loop
    grid_len_in_inches = convert_EV3_units_to_inches( length_of_side_on_occupency_grid )
    did_sensor_find_wall=did_sensor_detect_a_wall( x_robot, y_robot, dir_robot,        radii_of_sensored_object, tolerance_to_call_distances_the_same,        board, grid_len_in_inches )
    
    
    
    if (did_sensor_find_wall == 0) & (radii_of_sensored_object < 1.2)
        %x_bot=10;
        %y_bot=10;
        %dir_bot=45;
        num_radii=1;     %%%%%***change later to make generic
        for i=1:num_radii
            radius=radii_of_sensored_object(i);
            board=get_circular_arc_for_drawing( x_robot, y_robot, dir_robot,       radius, arc_theta, thickness_of_arc_to_draw,     board );
        end
    end
    
    
    
    sum(sum(board))
    
    %breakpoint: look at board at this point
    breakpoint=1;
    
end
