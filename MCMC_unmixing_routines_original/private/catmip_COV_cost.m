function cost=catmip_COV_cost(LLK,dbeta,COV_target)
% Compute COV misfit
%
% Sarah Minson, April 14, 2014
% Please cite:
% Minson, S. E., M. Simons, and J. L. Beck (2013), Bayesian inversion for finite fault earthquake source models I - theory and algorithm, Geophys. J. Int., 194(3), 1701-1726, doi:10.1093/gji/ggt180.

  COV=catmip_calc_COV_w(LLK,dbeta);
  cost=sqrt((COV-COV_target)^2);
  end
