function [ data ] = convert_data_log_from_inches_to_meters( data, x_col,y_col,sensor_col,std_dev_sensor_col )
%CONVERT_DATA_LOG_FROM_INCHES_TO_METERS Summary of this function goes here
%   Detailed explanation goes here
    data(:,x_col)=  convert_inches_to_EV3_units(  data(:,x_col)   );
    data(:,y_col)=  convert_inches_to_EV3_units(  data(:,y_col)   );
    data(:,sensor_col)=  convert_inches_to_EV3_units(  data(:,sensor_col)   );
    data(:,std_dev_sensor_col)=  convert_inches_to_EV3_units(  data(:,std_dev_sensor_col)   );

end

