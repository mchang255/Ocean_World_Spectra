function r = reflect(w,mu_0,mu)
%--------------------------------------------------------------------------
% CALCULATES REFLECTANCE 
% Inputs:
%   1) w = SSA
%   2) mu and mu_0 - cosines of incidence and emergence angles
% Outputs:
%   1) r = corresponding reflectance
% Dependences:
%   1) Chandrasekhar.m
%--------------------------------------------------------------------------

% Calculates Chandrasekhar of the mixture
H_mu0 = Chandrasekhar(w,mu_0);
H_mu = Chandrasekhar(w,mu);

% Calculates reflectance of the mixture
r = w/4/(mu_0+mu).*H_mu0.*H_mu;