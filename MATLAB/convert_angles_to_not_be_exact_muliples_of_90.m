function [ dir ] = convert_angles_to_not_be_exact_muliples_of_90( dir )
%CONVERT_ANGLES_TO_NOT_BE_EXACT_MULIPLES_OF_90 Summary of this function goes here
%   Detailed explanation goes here
    if dir==0 | dir==90 | dir==180 | dir==270  | dir==360
       dir=dir+.001;
    end

end

