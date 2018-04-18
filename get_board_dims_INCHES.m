function [  x_length_of_board_INCHES,y_length_of_board_INCHES  ] = get_board_dims_INCHES( board,length_of_grid_square_in_inches )
%GET_BOARD_DIMS_INCHES Summary of this function goes here
%   Detailed explanation goes here
    [n_squares_on_y_in_board,n_squares_on_x_in_board] = size(board);
    x_length_of_board_INCHES=n_squares_on_x_in_board*length_of_grid_square_in_inches;
    y_length_of_board_INCHES=n_squares_on_y_in_board*length_of_grid_square_in_inches;


end

