function p=catmip_llk2pdf(llk)
% p=catmip_llk2pdf(llk)
% Convert vector of log-likelihoods to normalized probabilities s.t.
% sum(p)=1.
%
% Sarah Minson, April 14, 2014
% Please cite:
% Minson, S. E., M. Simons, and J. L. Beck (2013), Bayesian inversion for finite fault earthquake source models I - theory and algorithm, Geophys. J. Int., 194(3), 1701-1726, doi:10.1093/gji/ggt180.

ln_sumP=llk(1);
for i=2:length(llk)
  ln_sumP=catmip_logSum(ln_sumP,llk(i));
end

llk_normalized=llk-ln_sumP;

p=exp(llk_normalized);

return
