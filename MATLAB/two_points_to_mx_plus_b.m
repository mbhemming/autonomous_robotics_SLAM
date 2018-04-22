function [ m,b ] = two_points_to_mx_plus_b(  x1,y1,x2,y2  )
%TWO_POINTS_TO_MX_PLUS_B Summary of this function goes here
%   Detailed explanation goes here
    m=(y1-y2)/(x1-x2);
    b=y1-m*x1;

end

