function [ theta ] = atan2_in_degrees_as_magnitude( delta_y, delta_x )
%ATAN2_IN_DEGREES Summary of this function goes here
%   Detailed explanation goes here
    theta=atan2(  abs( delta_y), abs( delta_x)  );
    theta= to_degrees(theta);

end

