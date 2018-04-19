function [ board ] = init_board( y_len_INCHES,x_len_INCHES, grid_square_len_INCHES )
%INIT_BOARD Summary of this function goes here
%   Detailed explanation goes here

%make these in quater of an inch inrements
length_of_enviroment_Y=convert_inches_to_EV3_units(y_len_INCHES);     
width_of_enviroment_X=convert_inches_to_EV3_units(x_len_INCHES);

length_of_side_on_occupency_grid=convert_inches_to_EV3_units(grid_square_len_INCHES);


board=zeros(    int32(length_of_enviroment_Y/length_of_side_on_occupency_grid),  int32(width_of_enviroment_X/length_of_side_on_occupency_grid)  );



end

