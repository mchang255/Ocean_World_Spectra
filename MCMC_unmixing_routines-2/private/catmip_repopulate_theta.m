function [theta,LLK]=catmip_repopulate_theta(theta,LLK,count);
% [theta,LLK]=catmip_repopulate_theta(theta,LLK,count)
%
% Repopulate theta and LLK matrices according to frequencies in count
%
% Sarah Minson, April 14, 2014
% Please cite:
% Minson, S. E., M. Simons, and J. L. Beck (2013), Bayesian inversion for finite fault earthquake source models I - theory and algorithm, Geophys. J. Int., 194(3), 1701-1726, doi:10.1093/gji/ggt180.

N=size(theta,2);
if size(LLK,2)~=N; error('theta and LLK mismatch in repopulate_theta'); end
if length(count)~=N; error('theta and count mismatch in repopulate_theta'); end
if sum(count)~=N; error('sum(count)~=N in repopulate_theta'); end

col=[];
for i=1:N
  col=[col repmat(i,1,count(i))];
end
if length(col)~=N; error('length(col)~=N in repopulate_theta'); end

theta=theta(:,col);
LLK  =  LLK(:,col);

end
