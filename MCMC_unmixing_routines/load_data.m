function D = load_data(file)

%-------------------------------------------------------------------------
% INPUT PARAMETERS
%-------------------------------------------------------------------------

% MINERAL ENDMEMBERS
rho = [2.31 2.85 2.71]'; % *** Density vector
% *** Load optical constants for each laboratory endmember; these are three
% columns matrices (wavelengths in meters, n, and k)
P{1} = dlmread('gypsum.txt');
P{2} = dlmread('dolomite.txt');
P{3} = dlmread('calcite.txt');
N = length(P);
% Sort them into n (real) and k (imaginary) refractive indices
for i =1:N
    O =P{i};
    l=O(:,1);
    nn=O(:,2);
    kk=O(:,3);
    lambda{i}=l;
    n{i}=nn;
    k{i}=kk;
    clear O l nn kk
end

% MCMC PARAMETERS
Nm = 2000;      % *** Length of each Markov chain; 
Nsteps = 10;   % *** Number of samples per cooling step
prior_size_low =[10 10 10]; % *** Low bounds on unif prior for size in microns
prior_size_high = [800 800 800]; % *** High bounds on unif prior for size in microns
prior_alpha= ones(1,length(rho)); % Alpha parameter for each component; taken as uniform as descibed in Lapotre et al. (2017); can be modified if necessary
% Note that currently proposal PDF draws from Dirichlet distribution
% using same alpha_i as the prior PDF.  This can be edited if necessary.
% (Dirichlet distribution: http://en.wikipedia.org/wiki/Dirichlet_distribution)
Ncomponents = length(rho); % Number of components = length(theta)/2

% SPECTRAL DATA
R1_vs_SSA0 = 1; % *** If reflectance data, set to 1; if SSA, set to 0;
if R1_vs_SSA0
    inc = 20; % *** incident angle for data reflectance spectrum
    e = 35; % *** emission angle for data reflectance spectrum
else
    inc = NaN;
    e = NaN;
end
S = dlmread(file); % *** Data (two columns matrix with wavelength and reflectance/SSA)
lam_SPEC = S(:,1);                   
R_SPEC = S(:,2);      
if min(lam_SPEC)>1
    lam_SPEC = lam_SPEC.*1e-9;      
end

% FIT PARAMETERS
Cov = 0.0005; % *** Covariance matrix = (Cd + Cp); increase to allow for more variance
min_lam = 0.8.*1e-6; % Minimum wavelength of range over which spectral fit is performed, in meters
max_lam = 2.5.*1e-6; % Maximum wavelength of range over which spectral fit is performed, in meters
% Note: Data and endmember spectra needed over this wavelength range

% Creating Data Structure
D.inc = inc;
D.e = e;
D.rho = rho';
D.lambda = lambda;
D.n = n;
D.k = k;
D.lam_SPEC = lam_SPEC;
D.R_SPEC = R_SPEC;
D.rho=rho'; 
D.Cinv = 1/Cov; 
D.Ncomponents = Ncomponents; 
D.prior_size_low = prior_size_low; 
D.prior_size_high = prior_size_high; 
D.prior_alpha = prior_alpha; 
D.Nm = Nm;
D.Nsteps = Nsteps;
D.R_vs_SSA = R1_vs_SSA0;
D.lmin = min_lam;
D.lmax = max_lam;