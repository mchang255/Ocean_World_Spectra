function [theta,LLK,nAccept,nReject]=run_metro_dirichlet(count,theta,LLK,Nsteps,Sm,beta,D,C,IOparallel)
% [theta,LLK,nAccept,nReject]=run_metro_dirichlet(count,theta,LLK,Nsteps,Sm,beta,D,C,IOparallel)
% Run Metropolis sampler
% Edited so that second half of theta vector is explored using Dirichlet
% proposal PDF.
%
% Sarah Minson, May 27, 2014
% Please cite:
% Minson, S. E., M. Simons, and J. L. Beck (2013), Bayesian inversion for finite fault earthquake source models I - theory and algorithm, Geophys. J. Int., 194(3), 1701-1726, doi:10.1093/gji/ggt180.


  N=size(theta,2);
  [nAccept,nReject]=deal(0);
  
  LLK(1,:) = [beta*LLK(2,:)] + LLK(3,:); % Update probabilities with new beta
  
  [theta,LLK]=catmip_repopulate_theta(theta,LLK,count);
  
  if IOparallel
    parfor i=1:N
      [mytheta,myLLK,mynAccept,mynReject]=catmip_metro_sample_dirichlet(theta(:,i),LLK(:,i),Nsteps,Sm,beta,D,C);
      theta(:,i)=mytheta(:,end); LLK(:,i)=myLLK(:,end);
      nAccept=nAccept+mynAccept; nReject=nReject+mynReject;
    end
  else
    for i=1:N
      [mytheta,myLLK,mynAccept,mynReject]=catmip_metro_sample_dirichlet(theta(:,i),LLK(:,i),Nsteps,Sm,beta,D,C);
      theta(:,i)=mytheta(:,end); LLK(:,i)=myLLK(:,end);
      nAccept=nAccept+mynAccept; nReject=nReject+mynReject;
    end
  end
  
  
  end
