function [x,LLK,Naccept,Nreject]=catmip_metro_sample_dirichlet(x0,llk0,N0,Sm,beta,D,C)
% [theta_new,P,Naccept,Nreject] = catmip_metro_sample_dirichlet(theta,theta_lead,Nsamples,myfun,sigma);
% myfun returns log likelihood
% Edited so that second half of theta vector is explored using Dirichlet
% proposal PDF.
%
% Sarah Minson, May 27, 2014
% April 14, 2015: Bug fix to make proposal PDF symmetric.  Now q is a
% uniform Dirichlet distribution.
% Please cite:
% Minson, S. E., M. Simons, and J. L. Beck (2013), Bayesian inversion for finite fault earthquake source models I - theory and algorithm, Geophys. J. Int., 194(3), 1701-1726, doi:10.1093/gji/ggt180.
  
Naccept = 0; Nreject = 0;

Nparam=length(x0); x=zeros(Nparam,N0);

x(:,1)=x0; LLK=zeros(3,N0); LLK(:,1)=llk0;
Sm0=Sm; Sm=eye(Nparam); Sm(1:2,1:2)=Sm0(1:2,1:2);
z=mvnrnd(zeros(Nparam,1),Sm,N0)';

%z=mvnrnd(zeros(Nparam/2,1),Sm(1:Nparam/2:1:Nparam/2),N0)';
z2=dirichletrnd_exc(ones(size(D.prior_alpha)),N0);

%%%%target=[75.0000  250.0000    0.1000    0.9000]';

for k=1:N0-1 % sample posterior for this level of tempering
  %if ~mod(k,5000); disp(['k=' num2str(k)]); end
  y=x(:,k) + z(:,k);
  y(Nparam/2+1:end)=z2(:,k); % Replace bottom half with Dirichlet sample
  %%%%y(3:end)=target(3:end);
  
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
