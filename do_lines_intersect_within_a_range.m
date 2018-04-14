function [ x_int,y_int ] = do_lines_intersect_within_a_range( l1x1,l1y1,l1x2,l1y2, l2x1,l2y1,l2x2,l2y2 )
%DO_LINES_INTERSECT Summary of this function goes here
%   l1x1 means line 1 and the x coordinate of point 1
% will output 1 if the first line intersects the second line in between the
% points that define it

%get the two lines in y=mx+b form
[m1,b1]=two_points_to_mx_plus_b(  l1x1,l1y1,l1x2,l1y2  );
[m2,b2]=two_points_to_mx_plus_b(  l2x1,l2y1,l2x2,l2y2  );

%find intersections
[ x_int,y_int ] = find_intersection_point_of_two_mx_plus_b_lines( m1,b1,m2,b2 );

if (min(l2x1,l2x2) <=x_int) && (x_int <= max(l2x1,l2x2)) && (min(l2y1,l2y2) <=y_int) && (y_int <= max(l2y1,l2y2))
    
else
    %9999 is used because it is bigger than the orders of magnitude that we
    %are using. It indicates the edge of the object wasn't hit
    x_int=9999;
    y_int=9999;
end


end

