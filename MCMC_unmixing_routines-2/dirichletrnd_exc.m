function x=dirichletrnd_exc(alpha,N)
% x=dirichletrnd_exc(alpha,N)
% Dirichlet random number generator on open interval (0, 1)

k=length(alpha);
for i=1:k
  x(i,:)=gamrnd(alpha(i),1,1,N);
end
x=x./repmat(sum(x),k,1);

i=find(x==0); x(i)=eps;
i=find(x==1); x(i)=1-eps;
