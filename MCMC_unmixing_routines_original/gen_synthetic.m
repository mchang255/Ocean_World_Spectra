function M = gen_synthetic(AB,d,R_vs_SSA)


if sum(AB)>1, AB = AB./100; end

% Load optical constants for each laboratory endmember
D=load_data;
rho = D.rho;
n = D.n;
k = D.k;
lambda = D.lambda;
inc = D.inc;
e = D.e;
f = wtperctof(rho',d,AB);

[lam,w] = Hapke_opt_forward(f,d,n,k,lambda);

if R_vs_SSA
    mu0 = cos(inc*pi/180);
    mu = cos(e*pi/180);
    w = reflect(w,mu0,mu);
end

M = [lam' w];

breakpoint = 1;