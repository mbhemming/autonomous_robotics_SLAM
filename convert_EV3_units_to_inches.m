function [ out ] = convert_EV3_units_to_inches( ev3_units )
%CONVERT_EV3_UNITS_TO_INCHES Summary of this function goes here
%   Detailed explanation goes here

    out = (2/0.6254)*ev3_units*12;
end

