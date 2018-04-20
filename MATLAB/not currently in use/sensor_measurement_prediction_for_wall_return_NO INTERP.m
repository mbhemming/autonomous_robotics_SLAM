function [ out ] = sensor_measurement_prediction_for_wall_returnNO_INTERP( altitude , theta )
%SENSOR_MEASUREMENT_PREDICTION_FOR_WALL_RETURN Summary of this function goes here
%   Under the assumption that we are far enough away from the corner to no
%   pic it up, then what is the expected sesnor measuremnt

error_value=-99; %We don't want the function to atempt to read certain extreme values. So these are inserted here
e_v=error_value; %re-nameing

%this is an array storing a matematical function. You put in the altitude
%from a way and the angle 
function_row_is_theta_col_is_altitude= [0.1700	0.1734	0.1752	0.1950	0.3245	2.5500;
                                       0.3210	0.3210	0.3259	0.3291	0.3869	2.5500;
                                       0.4740	0.4707	0.4861	0.5069	0.5370	2.5400;
                                       0.6254	0.6341	0.6389	0.6467	0.6676  e_v;
                                       0.7739	0.7727	0.7759	0.8391  e_v     e_v;
                                       0.9304	0.9727	0.9976  e_v     e_v     e_v;
                                       1.0771	1.1117  e_v     e_v     e_v     e_v;
                                       1.2229   e_v     e_v     e_v     e_v     e_v];
                                      
col=   int32(   ( roundn(theta,10)/10 ) +1   );
row=   int32(round(altitude/0.5));

out = function_row_is_theta_col_is_altitude(row,col);

if out==error_value
    error('warning: The bot is attempting a measurement outside its allowed parameters');
elseif  out > 2.5   
    out=out;
else
    out=out;
end

end

