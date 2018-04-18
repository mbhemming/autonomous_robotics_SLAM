
clear all;

mylego = legoev3('USB');

mysonicsensor = sonicSensor(mylego);

%set up%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


num_sensor_readings_for_a_given_robots_state=100;
tolerance_for_grouping_distance_as_the_same=.5;  %how close the measurment must be to be a hit
thickness_of_arc_to_draw=4;  %seems logical
arc_theta=60;  %the total sweep of the cone

length_of_side_on_occupency_grid=convert_inches_to_EV3_units(0.25);

%make these in quater of an inch inrements
length_of_enviroment_Y=convert_inches_to_EV3_units(69.75);     %***these are in the robots units. We can make them in inches later
width_of_enviroment_X=convert_inches_to_EV3_units(81.5);

tolerance_to_call_distances_the_same=convert_inches_to_EV3_units(4);  

%%%%%%***ad the sensor's position in relation to the robots centre
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
board=zeros(    int32(length_of_enviroment_Y/length_of_side_on_occupency_grid),  int32(width_of_enviroment_X/length_of_side_on_occupency_grid)  );

dummy_value=9999;
robot_state_x_y_direction=[dummy_value dummy_value dummy_value];  %initializing this variable but it will be over-written

sensor_readings=zeros(num_sensor_readings_for_a_given_robots_state,1);
i=1;

x=48;
y=33.25;
d=30;
%   y=69.75-24;
%  d=0;

%x: 0
%y: 33.25

while 1==1
    
    %break_point=dummy_value;  %set breakpoint here and manually type in the robots state
    breakpoint=1;
    x_robot_EV3UNITS=convert_inches_to_EV3_units( x );
    y_robot_EV3UNITS =convert_inches_to_EV3_units( y );
    dir_robot_DEGREES=d;
    
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
    %radii_of_sensored_object_EV3=get_radii_of_prospective_objects( sensor_readings );
    radii_of_sensored_object_EV3=mean(sensor_readings);
    %radii_of_sensored_object_EV3=convert_inches_to_EV3_units( 12 * sin(30*3.14/180) ) ;
    
    %test to see if the radii(sensor return) is actually a return from a
    %wall
    did_sensor_find_wall=0; %reset on each loop
    grid_len_in_inches = convert_EV3_units_to_inches( length_of_side_on_occupency_grid )
    
    %%%%%%%%%%%%%deciding if we should draw out the sensed object
    min_radius_to_draw_at=1.2;
    
    %if the sensed object(or possibly wall) is too far, then we won't draw
    %if
    if radii_of_sensored_object_EV3 < min_radius_to_draw_at
        is_sensor_model_applicable= FUNCTION
        if is_sensor_model_applicable==1
            did_sensor_find_wall=did_sensor_detect_a_wall( x_robot_EV3UNITS, y_robot_EV3UNITS , dir_robot_DEGREES,        radii_of_sensored_object_EV3, tolerance_to_call_distances_the_same,        board, grid_len_in_inches ) 
            if ( (did_sensor_find_wall == 0)
                radius_EV3=radii_of_sensored_object_EV3(i);
                board=get_circular_arc_for_drawing( x_robot_EV3UNITS, y_robot_EV3UNITS , dir_robot_DEGREES,       radius_EV3, arc_theta, thickness_of_arc_to_draw,     board,grid_len_in_inches );
            end
        else %if the sensor model isn't applicable then we use a heuristic to get the minimum distance we expect a wall to be
            
        end
        
    
    end
    
    %did_sensor_find_wall=0;
    
    end
    
    
    
    
    
    
    
    sum(sum(board))
    
    %breakpoint: look at board at this point
    breakpoint=1;
    
end
