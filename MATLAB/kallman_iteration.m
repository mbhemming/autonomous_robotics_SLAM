function [ mu_x,mu_y,S_x,S_y ] = kallman_iteration( theta,   mu_x,mu_y,S_x,S_y,    z )
%KALLMAN Summary of this function goes here
%   Detailed explanation goes here
%z is the sensor model

Q=
R=


A=1;
B=0;   %cotrols are perpendicular to the filtered direction
C= slope relating the units sensed to units in sensor model. IF the same then C=1;
D=0;  %the control doesn't effect the sensor readings

%   get the wall that gets hit
[ intersect_left, intersect_right, intersect_bottom, intersect_top ] = which_wall_will_the_robots_direction_collide_with(x_bot,y_bot,    dir_x_component, dir_y_component,   x_board_top_corner_INCHES,y_board_top_corner_INCHES  )

%   error check
if (intersect_left + intersect_right + intersect_bottom + intersect_top) ~=1
    error('error');
end

%   determin which variable to update -- after finding the varible, the
%   sensor model must be modified too. For example, if you are taking
%   positive readings from the left wall then you increase x-coordinate but
%   if it's from the left wall then you decrease it
if (intersect_left + intersect_right) == 1
    update_variable_mu=mu_x;
    update_variable_S=S_x;
    
    if intersect_left==1
        z=z;
    else
        z=MAX_LENGTH_OF_BOARD-z;
    end
elseif (intersect_top + intersect_bottom) == 1
    update_variable_mu=mu_y;
    update_variable_S=S_y;
    
    if intersect_bottom==1
        z=z;
    else
        z=MAX_LENGTH_OF_BOARD-z;
    end
end

%   we don't actaully need u here. The control is in a direction perpendicular
%   to the direction and so B=0;
u=9999;

%   kallman%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%prediction update
mu_p=A*update_variable_mu + B*u;
s_p=A*update_variable_S*A' + Q;


%measurement update
K=s_p*C'*1/(C*s_p*C'+R);
%K=s_p*C'*inv(C*s_p*C'+R);

mu = mu_p + K*(z(i)-C*mu_p);      %%%%%%These indeices are different but in the slides they aren't
S = (1-K*C)*s_p;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if (intersect_left + intersect_right) == 1
    mu_x=mu;
    S_x=S;
    
elseif (intersect_top + intersect_bottom) == 1
    mu_y=mu;
    S_y=S
end


end

