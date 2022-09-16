function wi = nkDtowi(n,k,D,lambda)
%--------------------------------------------------------------------------
% CALCULATES SSA OF A COMPONENT FROM ITS OPTICAL CONSTANTS AND GRAIN SIZE
% Inputs:
%   1) n = real index of refraqction
%   2) k = imaginary index of refraction
%   3) D = grain size
%   4) lambda = wavelengths
%   Note: n,k and lambda are vectors of the same length
% Outputs:
%   1) wi = SSA of component i
%--------------------------------------------------------------------------

% Coefficient for internal attenuation by absorption-----------------------
alpha = 4*pi.*k./lambda;
%--------------------------------------------------------------------------

% Coefficient for internal attenuation by scattering-----------------------
s = 0;
%--------------------------------------------------------------------------

% Internal, diffusive reflectance inside a particle------------------------
ri = (1-sqrt(alpha./(alpha+s*ones(size(alpha)))))./(1+sqrt(alpha./(alpha+s*ones(size(alpha)))));
%--------------------------------------------------------------------------

% Average path length for spherical particles of diameter D----------------
Da = 2/3*(n(1)^2-1/n(1)*(n(1)^2-1)^(3/2))*D;
%--------------------------------------------------------------------------

% Particle internal transmission coefficient-------------------------------
theta = (ri+exp(-sqrt(alpha.*(alpha+s.*ones(size(alpha)))).*Da))./(1+ri.*exp(-sqrt(alpha.*(alpha+s.*ones(size(alpha)))).*Da));
%--------------------------------------------------------------------------

% Surface reflection coeffecient for externally incident light-------------
Se = ((n-1).^2+k.^2)./((n+1).^2+k.^2)+0.05.*ones(size(lambda));
%--------------------------------------------------------------------------

% Surface reflection coefficient for internally scattered light------------
St = 1.014.*ones(size(lambda))-4./(n.*(n+1).^2);
%--------------------------------------------------------------------------

% SSA of the component-----------------------------------------------------
wi = Se.*ones(size(lambda)) + (1-Se).*(1-St)./(ones(size(lambda))-St.*theta).*theta;
%--------------------------------------------------------------------------


