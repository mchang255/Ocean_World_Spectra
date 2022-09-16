function f = wtperctof(rhos,ds,wtperc)
%--------------------------------------------------------------------------
% CALCULATES RELATIVE CROSS-SECTION FROM ABUNDANCE, DENSITY AND GRAIN SIZES
% Inputs:
%   1) rhos = vector of mineral solid densities 
%   2) ds = vector of effective grain sizes
%   3) wtperc = vector of abundances in weight percent
% Outputs:
%   1) f = vector of fractional relative cross-sections
%--------------------------------------------------------------------------


sig = wtperc./rhos./ds;
f = sig./sum(sig);

