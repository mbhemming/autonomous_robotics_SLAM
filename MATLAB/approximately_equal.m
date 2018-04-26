function [ out ] = approximately_equal( n1, n2 )
%APPROXIMATELY_EQUAL Summary of this function goes here
%   tells you if two floating point numbers are very close

    if abs(n1-n2) < 0.01
        out =1;
    else
       out=0; 
    end

end

