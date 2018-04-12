function [ output_args ] = decompose_sensor_repeated_sensor_measurement_into_arc_ranges( array_of_sensor_measurements, delta_to_form_a_new_category )
%DECOMPOSE_SENSOR_REPEATED_SENSOR_MEASUREMENT_INTO_ARC_RANGES Summary of this function goes here
%   When repeated sensor measuremnts are taken, we would like to sort
%   through that array of measurments and get out a list of distance(radii)
%   for the arcs. The issue is that some sensor measurments are close and
%   we want to group them into the same class. WHile other measuremnts are
%   outliers or don't make sense and we want to toss them out,

    n=length(array_of_sensor_measurements);

    %sort the array
    sorted_array_of_sensor_measurements=sort(array_of_sensor_measurements);
    
    
    radii_set=sorted_array_of_sensor_measurements(1); %add the first radius to the set
    
    curr_radii_category_starts_at_index=1;
    for i=1:n-1
        if sorted_array_of_sensor_measurements(i+1) - sorted_array_of_sensor_measurements(i+1) < delta_to_form_a_new_category
           %Do nothing for now. If we want more percision later then we   
        else
            
        end
    end
end

