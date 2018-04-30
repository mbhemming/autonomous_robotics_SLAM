%note: the kallman filter shouldn't be used if we arn't sure we are
%measumrening a wall.



%variance
%original Q and R
%Q=0.00005; %*100000;
%R=0.006;

n_data_points=4
%keeping both components seperate. This is unlike sample code we have seen
%so far but will allow us to update one paramter at a time
mu_y=    %**must init these to starting coordinates
mu_x=





Sx=init
Sy=init





for each waypoint
    
    
    %this might be confusing why we are applying the control while outside
    %the kallman_iteration. That is because our motion is perpendicular to
    %the dimension that the kallman is adjusting. There may indeed be error
    %acculating in the dimension that the kallman isn't filtering for but
    %we will have a chance to correct for that error after making the next
    %turn and taking readings in that dimension.
    u=  move to next corner waypoint . So mu_x=mu_x+delta_x_to_new_path or So mu_y=mu_y+delta_y_to_new_path
    
    [ mu_x,mu_y,S_x,S_y ] = kallman_iteration( theta,   mu_x,mu_y,S_x,S_y,    z )
    

end

%%%%%%%%%%ploting%%%%%%%%%%%%

%plotting simulated position
hold on;

plot_x=zeros(t_total/dt+1);
i=1;
for t=1:dt:t_total+1
    plot_x(i)=x(1,1,i);
    i=i+1;
end
scatter(1:dt:t_total+1,plot_x(:,1));

%%%%%%%%%
%plotting velocity
% plot_v=zeros(t_total/dt+1);
% i=1;
% for t=1:dt:t_total+1
%     plot_v(i)=x(2,1,i);
%     i=i+1;
% end
% scatter(1:dt:t_total+1,plot_v(:,1));

%%%%%%%%%%%

%plotting
plot_z=zeros(t_total/dt+1);
i=1;
for t=1:dt:t_total+1
    plot_z(i)=z(1,1,i);
    i=i+1;
end
%scatter(1:dt:t_total+1,plot_z(:,1));

%%%%%%%%%%%%%%%%%%%%%%%
%plotting filtered position

plot_mu=zeros(t_total/dt+1);
i=1;
for t=1:dt:t_total+1
    plot_mu(i)=mu(1,1,i);
    i=i+1;
end

scatter(1:dt:t_total+1,plot_mu(:,1));