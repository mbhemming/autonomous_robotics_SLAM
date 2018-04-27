%%%%%%%%%%% README

%   - This is the entry point for doing object localization
%   1) DATA: Import data -- STATE and SENSOR READINGS
%   2) INFORMATION: Comput properties for each tuple. An example of a property
%   is....is_a_wall_detected. 
%   3) GRID#1: Compute a grid for accounting how many times a grid square was
%   obserserved. Increment the whole cone
%   4) Filter data for certain properties.
        % example of simple filter: Filter for senor ranges less than about 3 ft. 
        %complex filter: Ignore measurements when the sensor model applie and the sensor has detectd a wall.
%   5) optinal: update a wight paramter. For instance, you could penalize
%   further away measmrements.
%   6) GRID#2: Compute occupency grid for obejcts based on arcs
%   7) OCCUPENCY GRID: Combine GRID#1 and GRID#2 to leverage both positive and negative
%   information.
%   8) Post processing of OCCUPENCY GRID.
%   9) Draw the OCCUPENCY GRID



%%%%%%%%%%%%%%%%%%%%%%    SETUP     %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%add properites params
smart_wall_detection=0;   % given that we know where the walls are setting this property allow us 
x_init=0;
y_init=0;

sensor_reading_max_allowed=1.0;
std_dev_sensor_reading_max_allowed=0.01;

fileter_away_occupency_grid_below=0.5;


%standard config
theta_for_arc=60;
line_thickness=4;
grid_len_INCHES=0.25;
y_len_INCHES=69.75;
x_len_INCHES=81.5;
board_object_localization= init_board( x_len_INCHES,y_len_INCHES, grid_len_INCHES );
board_counting_num_times_squares_were_seen= init_board( x_len_INCHES,y_len_INCHES, grid_len_INCHES );
tolerance_to_call_distances_the_same=convert_inches_to_EV3_units(9);

%%%%%%%%      load the data and append extra parameters for database properties   %%%%%%%%%%%%%%


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

%get data
data= csvread('rawSonarData.csv');
[n_rows n_cols] = size(data);
data = convert_data_log_from_inches_to_meters( data, x_col,y_col,sensor_col,std_dev_sensor_col );

%removing data that is out of range
data(  ~(data(:, x_col) < 2.04) , :)= [];
data(  ~(data(:, y_col) < 1.76) , :)= [];
data(  ~(data(:, x_col) > 0.04) , :)= [];
data(  ~(data(:, y_col) > 0.04) , :)= [];

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



%%%%%%%%%%%%%%%%%%%%%      compute database property params %%%%%%%%%%%%%%%

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
    
    dir_sensor = convert_angles_to_not_be_exact_muliples_of_90( dir_sensor );
    
    data(i,does_sensor_model_applies_col)=does_sensor_model_apply(  x_robot, y_robot,dir_sensor, board_object_localization, grid_len_INCHES );
    data(i,did_sensor_model_find_walls_col)=did_sensor_detect_a_wall( x_robot, y_robot , dir_sensor,        sensor_range, tolerance_to_call_distances_the_same,        board_object_localization, grid_len_INCHES );
    
    data(i,does_heuristic_apply_col)= ~data(i,does_sensor_model_applies_col);  %the heuristic is used when the sensor model doesn't apply
    data(i,is_measurement_low_enough_that_its_not_a_wall_via_heuristic_col)=is_measurement_low_enough_that_we_are_sure_its_not_a_wall_FUNCT(  x_robot, y_robot , dir_sensor,        sensor_range,        board_object_localization, grid_len_INCHES ) ;
end


%%%%%%%%%%%     UPDATE THE BOARD THAT KEEPS TRACK OF HOW MANY TIMES A GRID
%%%%%%%%%%%     SQUARE WAS VIEWED

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
[n_rows n_cols] = size(data); %must re-write the dims because we have subtracted rows
for i=1:n_rows
   
    r=    data(i,sensor_col)     ;
    x_EV3=x_init+data(i,x_col);
    y_EV3=y_init+data(i,y_col);
    dir= data(i,dir_bot_col)+data(i,dir_sensor_col);
    weight_of_square=data(i,weight_col)
    
    %dir
    max_r=sensor_reading_max_allowed;
    
    board_counting_num_times_squares_were_seen=board_update_for_how_many_times_a_sqaure_was_seen(x_EV3,y_EV3,dir,   r,max_r,  theta_for_arc,  line_thickness, weight_of_square,   board_counting_num_times_squares_were_seen, grid_len_INCHES );
    %board_counting_num_times_squares_were_seen=board_update_for_how_many_times_a_sqaure_was_seen(x_EV3,y_EV3,90,   r,theta_for_arc,  line_thickness, weight_of_square,   board_counting_num_times_squares_were_seen, grid_len_INCHES );
    %contourf(board_counting_num_times_squares_were_seen);
end




%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%    elim data with conditionals -- FILTERS

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%   simple conditionals

data(  ~(data(:, sensor_col) < sensor_reading_max_allowed) , :)= [];
data(~(data(:, std_dev_sensor_col) < std_dev_sensor_reading_max_allowed)  , :)= [];

%   complex conditionals
data( (     (data(:,does_sensor_model_applies_col ) == 1) &  (data(:,did_sensor_model_find_walls_col ) == 1)  )  , :)= [];
data((     (data(:,does_heuristic_apply_col ) == 1) &  (data(:,is_measurement_low_enough_that_its_not_a_wall_via_heuristic_col ) == 0)  )  , :)= [];




%%%%%%%%%%%%    modify the weight of the reading based on heuristics

%modify weight based on how far the measurement is away
[n_rows n_cols] = size(data);
for i=1:n_rows
    data(i,weight_col)=  data(i,weight_col)* ( (2*sensor_reading_max_allowed - data(i,sensor_col))  / (2*sensor_reading_max_allowed));
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%    use data to draw o arcs

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


[n_rows_board,n_cols_board]=size(board_counting_num_times_squares_were_seen);

%change this board to close to zero so we don't get division by zero errors
board_counting_num_times_squares_were_seen=board_counting_num_times_squares_were_seen+0.0001*ones(n_rows_board,n_cols_board);

[n_rows n_cols] = size(data); %must re-write the dims because we have subtracted rows
for i=1:n_rows
   
    r=    data(i,sensor_col)     ;
    x_EV3=x_init+data(i,x_col);
    y_EV3=y_init+data(i,y_col);
    dir= data(i,dir_bot_col)+data(i,dir_sensor_col);
    weight_of_square=data(i,weight_col)
   
    %draw boards
    board_object_localization = get_circular_arc_for_drawing( x_EV3,y_EV3,dir,   r,theta_for_arc,  line_thickness, weight_of_square,   board_object_localization, grid_len_INCHES ); 
end


%%%%%%%%%%%%%   COMBINE BOTH BOARDS  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


board=board_object_localization./board_counting_num_times_squares_were_seen;



%%%%%%%%%%%%    post processing  -for example: do we fill in seqctions
%%%%%%%%%%%%    between points

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% cutoff=fileter_away_occupency_grid_below;
% board = filter_final_grid_for_squares_above_some_quantity( board, cutoff );

%squares above 100 percent hits shouldn't occur
cutoff=1.01;
board = filter_for_squares_below_some_quantity( board, cutoff );



%%%%%%%%%%%%    draw graphs %%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

HeatMap(board)
%contourf(board);
%contourf(board_object_localization);
%contourf(board_counting_num_times_squares_were_seen)
