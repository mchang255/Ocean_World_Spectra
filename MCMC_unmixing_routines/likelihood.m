function L = likelihood(theta,D,LLK_prior)

% theta is a vector that has N grain sizes followed by N abundances
% D is a structure containing the data D.rho, D.n, D.k, D_lam_SPEC,
% D.R_SPEC

theta=theta';
  
% MODEL ABUNDANCES AND GRAIN SIZES
N = length(theta)/2;                        % # of endmembers
sizes = theta(1:N);                         % abundances
abundances = theta(N+1:2*N);                % grain sizes

% ENDMEMBERS SPECIFIC DATA
densities = D.rho; % mineral endmembers densities
fi = wtperctof(densities,sizes,abundances); % get fractional surface area for mixing

lambda = D.lambda;
n=D.n;
k=D.k;
lam_SPEC = D.lam_SPEC;
R_SPEC=D.R_SPEC;
inc = D.inc;
e = D.e;
R_vs_SSA = D.R_vs_SSA;
lmin = D.lmin;
lmax = D.lmax;

% FORWARD MODEL
[lam_MIX,SSA_MIX] = Hapke_opt_forward(fi,sizes,n,k,lambda);   % Model the SSA of the mixture corresponding to theta

if R_vs_SSA
    mu0 = cos(inc*pi/180);      
    mu = cos(e*pi/180);
    R_MIX = reflect(SSA_MIX,mu0,mu);
else
    R_MIX = SSA_MIX;
end

ind = find(lam_SPEC>=lmin&lam_SPEC<=lmax);
R_int = interp1(lam_MIX,R_MIX,lam_SPEC(ind));
res=R_SPEC(ind)-R_int;
L = -0.5*res'*D.Cinv*res;