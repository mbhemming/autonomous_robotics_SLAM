
clear all;

mylego = legoev3('USB');

mysonicsensor = sonicSensor(mylego);

%set up%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


num_sensor_readings_for_a_given_robots_state=100;
tolerance_for_grouping_distance_as_the_same=.5;  %how close the measurment must be to be a hit
thickness_of_arc_to_draw=4;  %seems logical
arc_theta=60;  %the total sweep of the cone

length_of_side_on_occupency_grid=.02;
length_of_enviroment=1;     %***these are in the robots units. We can make them in inches later
width_of_enviroment=1;

%%%%%%***ad the sensor's position in relation to the robots centre
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
board=zeros(    int32(length_of_enviroment/length_of_side_on_occupency_grid)    );

dummy_value=9999;
robot_state_x_y_direction=[dummy_value dummy_value dummy_value];  %initializing this variable but it will be over-written

sensor_readings=zeros(num_sensor_readings_for_a_given_robots_state,1);
i=1;

while 1==1
    
    %make sure the vector is still 1x3
    catch_error_vector_size( robot_state_x_y_direction,1,3 )
    
    %get n sensor readings
    for i=1:num_sensor_readings_for_a_given_robots_state
        sensor_readings(i)=readDistance(mysonicsensor);
    end
    
    %Get the radii for the arcs
    radii=get_radii_of_prospective_objects( sensor_readings );
    
    %test to see if the radii(sensor return) is actually a return from a
    %wall************************
    
    %break_point=dummy_value;  %set breakpoint here and manually type in the robots state
    breakpoint=1;
    
    %x_bot=10;
    %y_bot=10;
    %dir_bot=45;
    num_radii=1;     %%%%%***change later to make generic
    for i=1:num_radii
        radius=radii(i);
        board=get_circular_arc_for_drawing( x,y,d,       radius, arc_theta, thickness_of_arc_to_draw,     board );
    end

    sum(sum(board))
    
    %breakpoint: look at board at this point
    breakpoint=1;
    
end
