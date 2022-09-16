function COV=catmip_calc_COV_w(LLK,dbeta)
% COV=catmip_calc_COV_w(LLK,dbeta)
% Compute C.O.V. of plausibility weights from data likelihood and dbeta
%
% Sarah Minson, May 7, 2014
% Please cite:
% Minson, S. E., M. Simons, and J. L. Beck (2013), Bayesian inversion for finite fault earthquake source models I - theory and algorithm, Geophys. J. Int., 194(3), 1701-1726, doi:10.1093/gji/ggt180.

  w=catmip_calc_w_unnorm(LLK,dbeta);
  COV=std(w)/mean(w);
  end
  
