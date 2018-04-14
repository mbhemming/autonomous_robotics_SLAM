function [ quad ] = get_quadrant( dir )
%GET_QUADRANT Summary of this function goes here
%   Detailed explanation goes here
     if (dir_robot < 0)  |  (dir_robot > 360)
       error('the function expects angles between 0 and 360'); 
    end

    if (0 <= dir) & (dir <= 90)
        quad=1;
    elseif (90 <= dir) & (dir <= 180)
        quad=2;
    elseif (180 <= dir) & (dir <= 270)
        quad=3;
    elseif (270 <= dir) & (dir <= 360)
        quad=4;
    else
        error('this line shouldnt exectue');
    end

end

