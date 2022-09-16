function llk = llk_prior(theta,D)

% theta is a vector that has N grain sizes followed by N abundances
% D is a structure containing the data D.rho, D.n, D.k, D_lam_SPEC,
% D.R_SPEC

% MODEL ABUNDANCES AND GRAIN SIZES
N = length(theta)/2;                   % # of endmembers
sizes = theta(1:N);                    % abundances
abundances = theta(N+1:2*N);           % grain sizes

llk=0;
for i=1:N % Grain sizes
    llk=llk+log(unifpdf(theta(i),D.prior_size_low(i),D.prior_size_high(i)));
end



return
