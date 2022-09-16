function [lam,w] = Hapke_opt_forward(fi,Di,n,k,lambda)
%--------------------------------------------------------------------------
% CALCULATES REFLECTANCE OF A MIXTURE FROM SPECTRA OF INDIVIDUAL COMPONENTS
% Inputs:
%   1) fi = vector of relative cross-sections
%   2) Di = vector of grain sizes
% Dependences:
%   1) nkDtowi.m
%   2) reflect.m
%   3) Chandrasekhar.m
%--------------------------------------------------------------------------

%--------------------------------------------------------------------------

% Grain size in microns
if Di(1)>10
    Di = Di.*1e-6;
end

% Linear mixture of individual SSA
% Define wavelength over which the mixture spectrum will be modeled
% (the wavelength range is limited by the shortest range in the spectra)
lm = [];
lM = [];
N = length(fi);
for i = 1:N
    lm = [lm min(lambda{i})];
    lM = [lM max(lambda{i})];
end

lm = max(lm);
lM = min(lM);

dd = mean(diff(lambda{1}));
dl = dd/2;
lam = lm:dl:lM;

% Calculate SSA for each component of the mixture and interpolate it in the
% wanted wavelengths
for i =1:N
    wi{i} = nkDtowi(n{i},k{i},Di(i),lambda{i});
    wif{i} = interp1(lambda{i},wi{i}',lam');
end

% Caltculate SSA of the mixture
w = zeros(size(wif{1}));
for i = 1:N
    w = w+fi(i).*wif{i};
end