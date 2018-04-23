%load the data and append extra parameters%%%%%%%%%%%%%%
% A= [ 5 3 3 1 4; 6 6 3 1 0; 6 2 2 2 0; 4 2 3 2 0; 1 1 1 1 2 ]
% A(A(:, 5)== 0, :)= []

data= csvread('20180422-194755_TestOutput.csv');

%I'm overriding this data to make it make sense in terms of the enviroment
theta_robot=0;
x_init=convert_inches_to_EV3_units(35);
y_init=convert_inches_to_EV3_units(35);

x_col=1;
y_col=2;
theta_bot_col=3;
theta_sensor_col=4;
sensor_col=5;

%standard config
theta_for_arc=60;
line_thickness=4;
grid_len_INCHES=0.25;
y_len_INCHES=69.75;
x_len_INCHES=81.5;
board= init_board( x_len_INCHES,y_len_INCHES, grid_len_INCHES );



[n dummy]=size(data);

for i=1:n
   
    r= convert_inches_to_EV3_units(    data(i,sensor_col)     );
    x_EV3=x_init+convert_inches_to_EV3_units(    data(i,x_col)    );
    y_EV3=y_init+convert_inches_to_EV3_units(    data(i,y_col)     );
    dir= data(i,theta_bot_col)+data(i,theta_sensor_col);
    
    if r <.8
        board = get_circular_arc_for_drawing( x_EV3,y_EV3,dir,   r,theta_for_arc,  line_thickness,    board, grid_len_INCHES ); 
    end
end


contourf(board);