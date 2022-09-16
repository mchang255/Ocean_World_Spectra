function H = Chandrasekhar(w,x)
%--------------------------------------------------------------------------
% CALCULATES CHANDRASEKHAR H FUNCTION
% Inputs:
%   1) w = SSA
%   2) x = mu or mu_0
% Outputs:
%   1) H = corresponding Chandrasekhar H-function
%--------------------------------------------------------------------------

gamma = sqrt(1-w);
r0 = (1-gamma)./(1+gamma);
H = (1-w.*x.*(r0+(1-2*r0.*x)/2.*log((1+x)./x))).^(-1);