function w=catmip_calc_w_unnorm(LLK,dbeta)
% w=catmip_calc_w_unnorm(LLK,dbeta)
% Compute unnormalized plausibility weights from data likelihood and dbeta
%
% Sarah Minson, April 14, 2014
% Please cite:
% Minson, S. E., M. Simons, and J. L. Beck (2013), Bayesian inversion for finite fault earthquake source models I - theory and algorithm, Geophys. J. Int., 194(3), 1701-1726, doi:10.1093/gji/ggt180.

  w=exp(LLK*dbeta);
  end
