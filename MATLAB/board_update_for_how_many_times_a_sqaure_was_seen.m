function [ board_out ] = board_update_for_how_many_times_a_sqaure_was_seen( x,y,dir,   r,max_r,   theta_for_arc,  line_thickness, weight ,  board, grid_len_INCHES )
%GET_CIRCULAR_ARC_FOR_DRAWING Summary of this function goes here
%   Detailed explanation goes here
%theta_sweep is the total sweep angle for the sensor between the most
%extreme clockwise and most extreme counter-clockwise lengths
%the x,y pair doesn't refer to a pixel, instead, it refers to a lattice
%point.
%Writes '1' to any location on the arc

%%%***could later have an increased density of points at an outer radius

%***add description of generatign the points outward

%we only count that we could have seen something if it is actually with the
%range that we could find a object
if r > max_r
   r=max_r; 
end

if (0 < dir) & (dir <60)
   test=1; 
end

%tuning
theta_res=1;
radius_res=0.001/2;  %used to draw points for the thickness of the bands
%r= int32(r);
%x= int32(x);
%y= int32(y);

[n_squares_on_y_in_board,n_squares_on_x_in_board] = size(board);
board_based_on_what_sensor_sees=zeros(n_squares_on_y_in_board,n_squares_on_x_in_board);

if mod(line_thickness,2) ~= 0
   error('choose a thickness that is divisible by 2 to avoid error'); 
end



lower_theta=dir-theta_for_arc/2;
dummy=9999;
x_curr=dummy;   
y_curr=dummy;
%ii=1;
for curr_theta=lower_theta:theta_res: int32((dir+theta_for_arc/2))  %for each angle

    %log(ii)=curr_theta;
    %ii=ii+1;
    
    lower_radius=0;
    upper_radius=r+radius_res*line_thickness/2;
    for curr_radius=lower_radius:radius_res:upper_radius
        
        if curr_radius > .15
           breakpoint=1; 
        end
        
        %get the point on the arc
        x_curr=x+curr_radius*cos(to_radians(double(curr_theta) ) );    %must convert theta to a double to avoid an error
        y_curr=y+curr_radius*sin(to_radians(double(curr_theta)    )   );
        
        %find what square to declare is on the arc
        x_of_the_hit_square=int32( x_curr/(  convert_inches_to_EV3_units(grid_len_INCHES))   );
        y_of_the_hit_square=int32(y_curr/(  convert_inches_to_EV3_units(grid_len_INCHES)));
        
        if(  is_point_outside_the_board( board, x_of_the_hit_square, y_of_the_hit_square )==1 )
            %do nothing
            test=1;
        else
            %update grid
            board_based_on_what_sensor_sees(y_of_the_hit_square,x_of_the_hit_square)=weight;
            
        end
        
        
    end
end

board_out=board+board_based_on_what_sensor_sees;

