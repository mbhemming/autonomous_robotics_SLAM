function [ board ] = filter_for_squares_above_some_quantity( board, cutoff )
%FILTER_FINAL_GRID_FOR_SQUARES_ABOVE_SOME_QUANTITY Summary of this function goes here
%   Detailed explanation goes here
%   Sets zero to all board posisions less than the cutoff
    [n_cols, n_rows]=size(board);

    for i=1:n_cols
       for j=1:n_rows
           if board(i,j) >= cutoff
              board(i,j)=0; 
           end
       end
    end
end




