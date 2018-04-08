function [ out ] = is_point_outside_the_board( board, x_point, y_point )
%IS_POINT_OUTSIDE_THE_BOARD Summary of this function goes here
%   Detailed explanation goes here
%this assumes a board with one corner at (0,0)
    board_size=size(board);
    
     if  ( x_point > board_size(1,2) )   |     ( y_point > board_size(1,1)) | ( x_point < 1 )   |     ( y_point < 1)    
          out=1;
     else
        out=0; 
     end

end

