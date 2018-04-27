%choose which file to load from
load('board_after_two_sweeps.mat','board');
%load('contour_map_every_inch_along_a_side','board');

%OPTIONAL: apply simple filter
cuttoff=15;
for i=1:50
    for j=1:50
        if board(i,j) < cuttoff;
            board(i,j)=0;
        end
    end
end

%plot contour map
contourf(board)