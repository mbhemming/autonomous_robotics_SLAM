function [ interpolated_value ] = sensor_measurement_prediction_for_wall_return( altitude_FEET , theta_wrt_altitude )
%SENSOR_MEASUREMENT_PREDICTION_FOR_WALL_RETURN Summary of this function goes here
%   Detailed explanation goes here
%Bilinear Interpolates theta_wrt_altitude and altitude_FEET Table 

x_interest = theta_wrt_altitude;
y_interest = altitude_FEET;

x = [0 10 20 30 40 50] + [0, ones(1,5)*0.001]; % Degree Axis of Table
y = [0 0.5 1 1.5 2 2.5 3 3.5 4 4.5 ] + [0, ones(1,9)*0.001]; % altitude_FEET Axis of Table

e_v = 99; 
%initialize x1 and x2 and y1 y2
x1 = e_v;
x2 = e_v;
y1 = e_v;
y2 = e_v;

%look up table
table = [  0       0    0     0      0  e_v;
          .17  .1734 .175  .195  .3245  e_v ; 
         .3210 .32   .3259 .3291 .3869  e_v ;
         .474  .47   .4861 .5069 .536   e_v; 
         .6254 .6341 .6389 .6467 .6676  e_v;
         .7739 .7727 .7759 .8391  e_v   e_v;
         .9304 .9727 .9976  e_v    e_v  e_v; 
         1.0771 1.117  e_v  e_v    e_v  e_v; 
         1.2229  e_v   e_v  e_v   e_v   e_v;
         e_v     e_v   e_v  e_v   e_v   e_v ];
     
no_error_found_theta_wrt_altitude = 0;
no_error_found_altitude_FEET = 0;

%need to find nearest x1 x2 points

 
 %check to see if value is less than 0 else proceed
 if (theta_wrt_altitude < 0 || altitude_FEET < 0)
     'angle or altitude value less than zero'
     interpolated_value = 99;
 else
        [c, xindex] = min(abs(theta_wrt_altitude-x));
        % see if value is altitude value is out of range if not proceed
            if (theta_wrt_altitude > 40)
             'theta_wrt_altitude out of range for table';
             interpolate_value = 99;
            else 
     
             no_error_found_theta_wrt_altitude = 1;
                 % find x1 and x2 for interpolation
                 if (theta_wrt_altitude-x(xindex)) >= 0
                       x1 = x(xindex);
                       x2 = x(xindex+1);
                       xindex = xindex;
                 else
                       x1 = x(xindex-1);
                       x2 = x(xindex);
                       xindex = xindex -1;
                 end 
             end
            %now find y values
            [c, yindex] = min(abs(altitude_FEET-y))
 
            if (altitude_FEET > 4)
                
                'altitude_FEET out of range for table';
                interpolated_value = 99;
                
            else
                
                no_error_found_altitude_FEET = 1;
                if ((altitude_FEET-y(yindex)) >= 0)
                    y1 = y(yindex);
                    y2 = y(yindex+1);
                    yindex = yindex;
                else
                    y1 = y(yindex-1);
                    y2 = y(yindex);
                    yindex = yindex-1;
                end 
            end
            
            %check to see if any values are out of table range
            if (table(yindex,xindex) == 99 || table(yindex,xindex+1) == 99 || table(yindex+1,xindex) == 99 || table(yindex+1,xindex+1) == 99)
            interpolated_value = 99;
            
            else
            % Interpolate in X-direction - uses equation https://en.wikipedia.org/wiki/Bilinear_interpolation
            if (no_error_found_altitude_FEET == 1 && no_error_found_theta_wrt_altitude == 1)
            fx_y1 = ((x2-x_interest)/(x2-x1))*table(yindex,xindex)+ (x_interest-x1)/(x2-x1)*table(yindex,xindex+1);
            fx_y2 = ((x2-x_interest)/(x2-x1))*table(yindex+1,xindex)+ (x_interest-x1)/(x2-x1)*table(yindex+1,xindex+1);

            interpolated_value = ((y2-y_interest)/(y2-y1))*fx_y1 + ((y_interest-y1)/(y2-y1))*(fx_y2);
            else
            interpolated_value = 99;
            end
            end
 end


