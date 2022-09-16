function [w,beta,dbeta,c] = catmip_calc_beta(LLK,beta,dbeta,cov_target)
% [w,beta,dbeta,c] = catmip_calc_beta(LLK,beta,dbeta,cov_target)
% Compute updated values for plausibility weights, beta, dbeta, and COV
% w is normalized.
%
% Sarah Minson, December 7, 2015
% Please cite:
% Minson, S. E., M. Simons, and J. L. Beck (2013), Bayesian inversion for finite fault earthquake source models I - theory and algorithm, Geophys. J. Int., 194(3), 1701-1726, doi:10.1093/gji/ggt180.

  x1=realmin;
  x2=1-beta;
  
  %cov_target = 1;
  
  LLK=LLK-median(LLK);
  
  covfun=@(dbeta)catmip_calc_COV_w(LLK,dbeta);
  
  % Test if small dbeta is enough
  test_dbeta = x2;
  test_COV=covfun(test_dbeta);
  if test_COV <= cov_target
      dbeta = test_dbeta;
  else
      % Find x2
      x2=dbeta;
      while covfun(x2)<cov_target; x2=2*x2; end
      x2=min([x2, 1-dbeta]);
      options = optimset('fminbnd');
      options = optimset(options,'FunValCheck','on','TolX',1e-12);
      disp(['Soving for dbeta on bounds [0 ' num2str(x2) ']']); options = optimset(options,'Display','iter');
      %dbeta = fminbnd(@(x)abs(covfun(x)-cov_target),x1,x2,options);
      dbeta = fminbnd(@(x)abs(covfun(exp(x))-cov_target),log(x1),log(x2),options);
      dbeta=exp(dbeta);
      
      %dbeta = fminbnd(@(x) catmip_COV_cost(wfun,dbeta,cov_target),x1,x2,options);
      %cost=sqrt((COV-COV_target)^2);
  end

  % Compute output values
  w=catmip_calc_w_normalized(LLK,dbeta);
  w_unnorm=catmip_calc_w_unnorm(LLK,dbeta);
  c=std(w_unnorm)/mean(w_unnorm);
  beta=beta+dbeta;
  
end
