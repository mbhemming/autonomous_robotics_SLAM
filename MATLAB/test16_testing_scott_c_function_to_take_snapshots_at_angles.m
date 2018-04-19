clear all;

mylego = legoev3('USB');

mysonicsensor = sonicSensor(mylego);

x_cord=.45;
y_cord=.45;
num_sensor_readings_for_a_given_robots_state = 100;
sweep_angle_max = 45;
angle_increment = 5;
motorRotate = motor(mylego,'C');

y_len_INCHES=69.75;
x_len_INCHES=81.5;
grid_square_len_INCHES=0.25; 
board= init_board( y_len_INCHES,x_len_INCHES, grid_square_len_INCHES );



%**add board

[board_temp_values] = gather_sensor_measurements_for_board(x_cord,y_cord,num_sensor_readings_for_a_given_robots_state,     sweep_angle_max,angle_increment,    mysonicsensor,motorRotate, board,grid_square_len_INCHES)

breakpoint=1;