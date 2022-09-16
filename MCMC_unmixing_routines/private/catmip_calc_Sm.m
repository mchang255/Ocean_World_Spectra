function Sm = catmip_calc_Sm(w,theta,Cmsqr)
% Sm = catmip_calc_Sm(w,theta,Cmsqr)
%
% Sarah Minson, April 14, 2014
% Please cite:
% Minson, S. E., M. Simons, and J. L. Beck (2013), Bayesian inversion for finite fault earthquake source models I - theory and algorithm, Geophys. J. Int., 194(3), 1701-1726, doi:10.1093/gji/ggt180.

p=w/sum(w);
E=sum([repmat(p,size(theta,1),1).*theta],2);
Sm=zeros(size(theta,1));
for i=1:size(theta,2); Sm=Sm+p(i)*theta(:,i)*theta(:,i)'; end
Sm=Sm-E*E';

Sm=Cmsqr*Sm;

return
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%
%PROCEDURE:
%1. Calculate p=w/sum(w)
%2. Calculate the expected value: E = sum(p_i*theta_i)
%3. Calcluate Sm = sum{p_i*theta_i*theta_i^T} - E*E^T
%4. Return Cm^2 * Sm
