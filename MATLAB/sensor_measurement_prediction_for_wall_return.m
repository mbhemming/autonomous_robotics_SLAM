function [ interpolated_value ] = sensor_measurement_prediction_for_wall_return( distance, angle )
%SENSOR_MEASUREMENT_PREDICTION_FOR_WALL_RETURN Summary of this function goes here
%   Detailed explanation goes here


%Bilinear Interpolates Angle and Distance Table 

x_interest = angle;
y_interest = distance;

x = [0 10 20 30 40 50]; % Degree Axis of Table
y = [0 0.5 1 1.5 2 2.5 3 3.5 4]; % Distance Axis of Table

e_v = 99; 
table = [ 0 0 0 0 0 0; .17 .1734 .175 .195 .3245 2.55; .3210 .32 .3259 .3291 .3869 2.55; .474 .47 .4861 .5069 .536 2.55 ; .6254 .6341 .6389 .6467 .6676 e_v; .7739 .7727 .7759 .8391  e_v e_v; .9304 .9727 .9976 e_v e_v e_v; 1.0771 1.117 e_v e_v e_v e_v; 1.2229 e_v e_v e_v e_v e_v];
no_error_found_angle = 0;
no_error_found_distance = 0;

%need to find nearest x1 x2 points
[c xindex] = min(abs(angle-x));
 
 if (angle > 49.99)
      'angle out of range for table'
      x1 = 99;
      x2 = 99;
      x3 = 99;
      x4 = 99;
 else 
 no_error_found_angle = 1;
 if (angle-x(xindex)) >= 0
     x1 = x(xindex);
     x2 = x(xindex+1);
     xindex = xindex;
 else
     x1 = x(xindex-1);
     x2 = x(xindex);
     xindex = xindex -1;
 end 
 end
%need to find nearest y1 y2 points
[c yindex] = min(abs(distance-y))
 
 if (distance > 3.99)
      'distance out of range for table'
      x1 = 99;
      x2 = 99;
      x3 = 99;
      x4 = 99;
 else 
 no_error_found_distance = 1;
 if (distance-y(yindex)) >= 0
     y1 = y(yindex);
     y2 = y(yindex+1);
     yindex = yindex;
 else
     y1 = y(yindex-1);
     y2 = y(yindex);
     yindex = yindex-1;
 end 
 end   
 
 % Interpolate in X-direction - uses equation https://en.wikipedia.org/wiki/Bilinear_interpolation
if (no_error_found_distance == 1 && no_error_found_angle == 1)
 fx_y1 = ((x2-x_interest)/(x2-x1))*table(yindex,xindex)+ (x_interest-x1)/(x2-x1)*table(yindex,xindex+1);
 fx_y2 = ((x2-x_interest)/(x2-x1))*table(yindex+1,xindex)+ (x_interest-x1)/(x2-x1)*table(yindex+1,xindex+1);
 
 interpolated_value = ((y2-y_interest)/(y2-y1))*fx_y1 + ((y_interest-y1)/(y2-y1))*(fx_y2);
elseif ((x1 == 99) || (x2 == 99) || (y1 == 99) || (y2 == 99 ))
interpolated_value = 99;
else
interpolated_value = 99;
end
end

