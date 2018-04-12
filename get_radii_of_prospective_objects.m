function [ category ] = get_radii_of_prospective_objects( sensor_reading )
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
% Create Categories From Ultrasonic Data Points



% Sorts Sensor Readings

sensor_reading = sort(sensor_reading);

%set tolerences

cat_tol = 0.02*2;

%Initialize Category

j = 1; % Used for incrementing categories
k = 2; % Used for temp averages

temp_cat(1) = sensor_reading(1) ;
category(1) = sensor_reading(1);

for i = 2:length(sensor_reading)
    
    temp_mean = mean(temp_cat);
    
    if (abs(sensor_reading(i)-temp_mean) < cat_tol)
        
        category(j) = temp_mean; %updates category with current mean
        temp_cat(k) = sensor_reading(i); %used for calculate next mean
        
    else
        
        %makes new category if conditions previous cat_tol condition met
        
        category(j) = temp_mean;
        
        j = j+1; % increases category
        k = 1; % resets temp_mean
        temp_cat = []; % clears temp_cat
        category(j) = sensor_reading(i);
        temp_cat(k) = sensor_reading(i);
        
    end
    
    k = k+1; %increments temp_cat
    
end

end

