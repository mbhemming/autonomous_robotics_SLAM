
% clear all;
% 
% mylego = legoev3('USB');
% 
% mysonicsensor = sonicSensor(mylego);

%set up%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

num_sensor_readings_for_a_given_robots_state=100;
tolerance_for_grouping_distance_as_the_same=.5;  %how close the measurment must be to be a hit
thickness_of_arc_to_draw=tolerance_for_grouping_distance_as_the_same;  %seems logical
arc_theta=60;  %the total sweep of the cone

length_of_side_on_occupency_grid;
length_of_enviroment=
width_of_enviroment=

%%%%%%***ad the sensor's position in relation to the robots centre

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

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
    
    %break_point=dummy_value;  %set breakpoint here and manually type in the robots state
    
    cluster_to_get_each_arc_to_draw();
end
