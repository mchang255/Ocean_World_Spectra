function [x,LLK,Naccept,Nreject]=catmip_metro_sample(x0,llk0,N0,Sm,beta,D,C)
% [theta_new,P,Naccept,Nreject] = catmip_metro_sample(theta,theta_lead,Nsamples,myfun,sigma);
% myfun returns log likelihood
%
% Sarah Minson, April 14, 2014
% Please cite:
% Minson, S. E., M. Simons, and J. L. Beck (2013), Bayesian inversion for finite fault earthquake source models I - theory and algorithm, Geophys. J. Int., 194(3), 1701-1726, doi:10.1093/gji/ggt180.
  
Naccept = 0; Nreject = 0;

Nparam=length(x0); x=zeros(Nparam,N0);

x(:,1)=x0; LLK=zeros(3,N0); LLK(:,1)=llk0;
z=mvnrnd(zeros(Nparam,1),Sm,N0)';
for k=1:N0-1 % sample posterior for this level of tempering
  %if ~mod(k,5000); disp(['k=' num2str(k)]); end
  y=x(:,k) + z(:,k);
  
  px=LLK(1,k);
  [LLKy,error_code]=catmip_llk_post(y,beta,D,C); py=LLKy(1);
  
  % r = py/px;
  r = exp(py-px);
  u=rand;
  
  if u<=r & ~error_code
    x(:,k+1)=y;     LLK(:,k+1)=LLKy;     Naccept=Naccept+1;
  else
    x(:,k+1)=x(:,k);LLK(:,k+1)=LLK(:,k); Nreject=Nreject+1;
  end
end
