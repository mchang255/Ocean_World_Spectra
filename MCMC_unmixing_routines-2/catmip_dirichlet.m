function [THETA,LLK_SAVE,ACC,REJ]=catmip_dirichlet(N,Nsteps,theta,D,llk_prior,for_model)
% [THETA,nAccept,nReject]=catmip_dirichlet(N,Nsteps,theta,D,C)
% CATMIP algorithm main
% Edited so that second half of theta vector is explored using Dirichlet
% proposal PDF.
%
% Sarah Minson, May 27, 2014
% Please cite:
% Minson, S. E., M. Simons, and J. L. Beck (2013), Bayesian inversion for finite fault earthquake source models I - theory and algorithm, Geophys. J. Int., 194(3), 1701-1726, doi:10.1093/gji/ggt180.

disp('Begin CATMIP')
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Initializaton
%ctarget = 1.00;         % target value for adaptive beta
btol    = 0.005;        % goal for convergence of sampler
%ctol    = 0.01*ctarget; % tolerance for beta calculation
Cmsqr   = 0.1*0.1;      % Scale factor for proposal PDF q(Cmsqr*Sm)
beta    = 0.0;          % cooling temperature
dbeta   = 5.e-5;        % initial guess for change in beta
cov_target = 1;         % target coefficient of variation
beta = 0; c = 0;
m=0;
ACC=0; REJ=0;
C.llk_prior=llk_prior;
C.for_model=for_model;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% Check initialization
if size(theta,2)~=N
  error(['theta must have N columns: size(theta,2)=' num2str(size(theta,2))...
	 ' N=' num2str(N)]);
end

Nparam=size(theta,1);
disp(['Number of model parameters: ' num2str(Nparam)]);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Run in serial or parallel?
if exist('parpool') == 2 % matlabpool function exists
  IOparallel = 1;
%  if ~parpool('size'); parpool open; end % Open matlabpool if none exists
if isempty(gcp('nocreate')); parpool; end
  disp('Parallel execution');
else
  IOparallel = 0;
  disp('Serial execution');
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Run forward model for prior samples
nAccept=0; nReject=0;
fprintf('m\tCm^2\tCOV\tbeta\t\tnAccept\t\tnReject\n');
fprintf('%d\t%.4f\t%.4f\t%.6e\t%.6e\t%.6e\n',...
	m,Cmsqr,c,beta,nAccept,nReject);
for i=1:N
  LLK(:,i)=catmip_llk_post(theta(:,i),beta,D,C);
end
THETA(:,:,m+1)=theta; LLK_SAVE(:,:,m+1)=LLK;
%assignin('base','THETA_SAVE',THETA);
%assignin('base','LLK_SAVE',LLK_SAVE);


while 1
  m=m+1;
  LLK0=LLK(2,:);
  assignin('base','LLK0',LLK0);
  %[beta,c,dbeta,w] = calc_beta(LLK0,beta,c,dbeta,m);
  [w,beta,dbeta,c]=catmip_calc_beta(LLK0,beta,dbeta,cov_target);
  assignin('base','LLK0',LLK0);
  assignin('base','beta',beta);
  assignin('base','dbeta',dbeta);
  assignin('base','cov_target',cov_target);
  assignin('base','theta',theta);
  
  fprintf('%d\t%.4f\t%.4f\t%.6e\t',m,Cmsqr,c,beta);
  
  Sm=catmip_calc_Sm(w,theta,Cmsqr);
  Sm = 0.5*(Sm + Sm'); % Symmetric???
  
  count=histc(rand([1 N]),[0 cumsum(w)]);
  count(end-1)=sum(count(end-1:end));
  count=count(1:end-1);
  
  [theta,LLK,nAccept,nReject]=catmip_run_metro_dirichlet(count,theta,LLK,Nsteps,Sm,beta,D,C,IOparallel);

  %  write_beta(m, Cmsqr, c, beta, 0.0, 0.0, fname);
  fprintf('%.6e\t%.6e\n',nAccept,nReject);
  THETA(:,:,m+1)=theta; LLK_SAVE(:,:,m+1)=LLK; ACC(m+1,1)=nAccept; REJ(m+1,1)=nReject;
  
  accRatio = nAccept/(nAccept + nReject);
  kc = (8*accRatio + 1)/9;
  % //kc = max(kc,0.2);   kc = min(kc,1);
  if (kc < 0.1); kc = 0.1; end
  if (kc > 1.0); kc = 1.0; end
  Cmsqr = kc * kc;
    
  if (1-beta < btol); fprintf('mstop=%d\n',m); break; end
  
end


end
