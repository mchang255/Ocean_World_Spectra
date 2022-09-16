function [Vllk,error_code]=catmip_llk_post(y,beta,data,C)
% [llk,error_code]=catmip_llk_post(y,beta,D,C)
%
% Sarah Minson, April 14, 2014
% Please cite:
% Minson, S. E., M. Simons, and J. L. Beck (2013), Bayesian inversion for finite fault earthquake source models I - theory and algorithm, Geophys. J. Int., 194(3), 1701-1726, doi:10.1093/gji/ggt180.

  error_code = 0;
  
  LLK_MIN = -inf;

  Vllk=nan*ones(3,1);

  %//---- UNWRAP THETA AND STORE VARIABLES IN DATA STRUCT ------
  %data=C.get_model(y,data);

  %//----------------- PRIOR P(m) -----------------------------
  LLK_prior = C.llk_prior(y,data);
  if ~isfinite(LLK_prior); error_code = -1; return; end


  %// ----------------- DATA FIT P(D|m) -----------------------
  %// llk = -0.5*(y-mu)'*Sinv*(y-mu);

  LLK = C.for_model(y,data, LLK_prior);
  if length(LLK)>1; LLK_prior=LLK(2); LLK=LLK(1); end
  if ~isfinite(LLK); printf('BAD FORWARD MODEL:\n'); disp(y);
    error_code = -2; return; end

  %//----------------- POSTERIOR P(m|D) -----------------------
  LLK_post = LLK_prior + (beta*LLK);

  %//----------------- STORE IN VECTOR ------------------------

  %// Vllk = log[P(m|D) P(D|m) P(m)] posterior, data fit, prior

  Vllk(1)=LLK_post;
  Vllk(2)=LLK;
  Vllk(3)=LLK_prior;

  return
  
