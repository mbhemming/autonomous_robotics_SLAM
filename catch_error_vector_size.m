function [  ] = catch_error_vector_size( vector,n_rows,n_cols )
%CATCH_ERROR_VECTOR_SIZE Summary of this function goes here
%   Detailed explanation goes here
    if(  size(vector)~=[n_rows n_cols] )
        error('ERROR: A vector has inappropriate dimensions'); 
    end

end

