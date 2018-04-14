function [ x,y ] = find_intersection_point_of_two_mx_plus_b_lines( m1,b1,m2,b2 )
%FIND_INTERSECTION_POINT_OF_TWO_MX_PLUS_B_LINES Summary of this function goes here
%   Detailed explanation goes here
    x=(b2-b1)/(m1-m2);
    y=m1*x+b1;

end

