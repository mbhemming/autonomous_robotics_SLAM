%add properites params
smart_wall_detection=0;   % given that we know where the walls are setting this property allow us 
x_init=convert_inches_to_EV3_units(35);
y_init=convert_inches_to_EV3_units(35);

sensor_reading_max_allowed=1.2;
std_dev_sensor_reading_max_allowed=0.01;

fileter_away_occupency_grid_below=1;


%standard config
theta_for_arc=60;
line_thickness=4;
grid_len_INCHES=0.25;
y_len_INCHES=69.75;
x_len_INCHES=81.5;
board= init_board( x_len_INCHES,y_len_INCHES, grid_len_INCHES );
tolerance_to_call_distances_the_same=convert_inches_to_EV3_units(4);

%load the data and append extra parameters%%%%%%%%%%%%%%
% A= [ 5 3 3 1 4; 6 6 3 1 0; 6 2 2 2 0; 4 2 3 2 0; 1 1 1 1 2 ]
% A(A(:, 5)== 0, :)= []

%cols
x_col=1;
y_col=2;
dir_bot_col=3;
dir_sensor_col=4;
sensor_col=5;
std_dev_sensor_col=6;

weight_col=7;

does_sensor_model_applies_col=8;
did_sensor_model_find_walls_col=9;

does_heuristic_apply_col=10;  %the heuristic is used when the sensor model doesn't apply
is_measurement_low_enough_that_its_not_a_wall_via_heuristic_col=11;

data= csvread('20180422-233150_TestOutput.csv');
[n_rows n_cols] = size(data);

%convert
data = convert_data_log_from_inches_to_meters( data, x_col,y_col,sensor_col,std_dev_sensor_col )
% data(:,x_col)=  convert_inches_to_EV3_units(  data(:,x_col)   );
% data(:,y_col)=  convert_inches_to_EV3_units(  data(:,y_col)   );
% data(:,sensor_col)=  convert_inches_to_EV3_units(  data(:,sensor_col)   );
% data(:,std_dev_sensor_col)=  convert_inches_to_EV3_units(  data(:,std_dev_sensor_col)   );


%add cols for weight parameter - this param will let you influence how much
%weight to give to this arc
for i=1:n_rows
    data(i,weight_col)=1;  %init weights to 1
end
%add cols for properties
for i=1:n_rows
    x_robot=x_init+data(i,x_col);
    y_robot=y_init+data(i,y_col);
    dir_sensor= data(i,dir_bot_col)+data(i,dir_sensor_col);
    sensor_range=data(i,sensor_col);
    
    if dir_sensor==0 | dir_sensor==90 | dir_sensor==180 | dir_sensor==270  | dir_sensor==360
       dir_sensor=dir_sensor+.001;
    end
    
    if abs(dir_sensor-90) < .1
       breakpoint=1; 
    end
    
    data(i,does_sensor_model_applies_col)=does_sensor_model_apply(  x_robot, y_robot,dir_sensor, board, grid_len_INCHES );
    data(i,did_sensor_model_find_walls_col)=did_sensor_detect_a_wall( x_robot, y_robot , dir_sensor,        sensor_range, tolerance_to_call_distances_the_same,        board, grid_len_INCHES );
    
    data(i,does_heuristic_apply_col)= ~data(i,does_sensor_model_applies_col);  %the heuristic is used when the sensor model doesn't apply
    data(i,is_measurement_low_enough_that_its_not_a_wall_via_heuristic_col)=is_measurement_low_enough_that_we_are_sure_its_not_a_wall_FUNCT(  x_robot, y_robot , dir_sensor,        sensor_range,        board, grid_len_INCHES ) ;
end

%load data
%data=

%add weight param





%sensor_model_applies=

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%    elim data with conditionals

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%simple conditionals
data(  ~(data(:, sensor_col) < sensor_reading_max_allowed) , :)= [];
% %data(data(:, 5)== 0, :)= []
data(~(data(:, std_dev_sensor_col) < std_dev_sensor_reading_max_allowed)  , :)= [];

%data(data(:, 5)== 0, :)= [];


%complex conditionals
% does_sensor_model_applies_col=8;
% did_sensor_model_find_walls_col=9;
% does_heuristic_apply_col=10;  %the heuristic is used when the sensor model doesn't apply
% is_measurement_low_enough_that_its_not_a_wall_via_heuristic_col=11;

data( (     (data(:,does_sensor_model_applies_col ) == 1) &  (data(:,did_sensor_model_find_walls_col ) == 1)  )  , :)= [];
data((     (data(:,does_heuristic_apply_col ) == 1) &  (data(:,is_measurement_low_enough_that_its_not_a_wall_via_heuristic_col ) == 0)  )  , :)= [];

%%%%%%%%%%%%    modify the weight of the reading based on heuristics

%modify weight based on how far the measurement is away
[n_rows n_cols] = size(data);
for i=1:n_rows
    data(i,weight_col)=  data(i,weight_col)* ( (sensor_reading_max_allowed - data(i,sensor_col))  / sensor_reading_max_allowed);
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%




%%%%%%%%%%%%    use data to draw

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
[n_rows n_cols] = size(data); %must re-write the dims because we have subtracted rows
for i=1:n_rows
   
    r=    data(i,sensor_col)     ;
    x_EV3=x_init+data(i,x_col);
    y_EV3=y_init+data(i,y_col);
    dir= data(i,dir_bot_col)+data(i,dir_sensor_col);
    
    board = get_circular_arc_for_drawing( x_EV3,y_EV3,dir,   r,theta_for_arc,  line_thickness,    board, grid_len_INCHES ); 

end






%%%%%%%%%%%%    post processing  -for example: do we fill in seqctions
%%%%%%%%%%%%    between points

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
cutoff=fileter_away_occupency_grid_below;
board = filter_final_grid_for_squares_above_some_quantity( board, cutoff )



%%%%%%%%%%%%    error checking

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%









%%%%%%%%%%%%    draw graphs

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
contourf(board);

%%%***should I have it so that I can configure many variants and draw
%%%multiple




