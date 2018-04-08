function [ board ] = get_circular_arc_for_drawing( x,y,dir,   r,theta_for_arc,  line_thickness, board )
%GET_CIRCULAR_ARC_FOR_DRAWING Summary of this function goes here
%   Detailed explanation goes here
%theta_sweep is the total sweep angle for the sensor between the most
%extreme clockwise and most extreme counter-clockwise lengths
%the x,y pair doesn't refer to a pixel, instead, it refers to a lattice
%point.
%Writes '1' to any location on the arc

%%%***could later have an increased density of points at an outer radius

%***add description of generatign the points outward

%tuning
theta_res=1;
radius_res=0.2;  %used to draw points for the thickness of the bands
%r= int32(r);
%x= int32(x);
%y= int32(y);

if mod(line_thickness,2) ~= 0
   error('choose a thickness that is divisible by 2 to avoid error'); 
end


lower_theta=dir-theta_for_arc/2;
dummy=9999;
x_curr=dummy;
y_curr=dummy;
for curr_theta=lower_theta:theta_res: int32((dir+theta_for_arc/2))  %for each angle
    lower_radius=int32(r-radius_res*line_thickness/2);
    upper_radius=int32(r+radius_res*line_thickness/2);
    for curr_radius=lower_radius:line_thickness:upper_radius
        %get the point on the arc
        x_curr=x+curr_radius*cos(to_degrees(  double(curr_theta)  ));    %must convert theta to a double to avoid an error
        y_curr=y+curr_radius*sin(to_degrees(     double(curr_theta)       ));
        
        %find what square to declare is on the arc
        x_of_the_hit_square=int32(x_curr);
        y_of_the_hit_square=int32(y_curr);
        
        if(  is_point_outside_the_board( board, x_of_the_hit_square, y_of_the_hit_square )==1 )
            %do nothing
        else
            %update grid
            board(x_of_the_hit_square,y_of_the_hit_square)=1;
        end
        
        
    end
end

