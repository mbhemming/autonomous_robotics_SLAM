clear all;

%%Test 1%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%expected outpout is an array of zeros with 1's at a radius of 5 for a
%quarter of a circle
board=zeros(20);

x_bot=10;
y_bot=10;
dir_bot=45;
r=5
theta_for_arc=90;
line_thickness=4;

get_circular_arc_for_drawing( x_bot,y_bot,dir_bot,       r, theta_for_arc, line_thickness,     board )
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 
% board=zeros(20);
% 
% 
% get_circular_arc_for_drawing( 1,1,45,   5,90,  4, board )