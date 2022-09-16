function c = catmip_logSum(a, b)
% logSum - Computer log(exp(a)+exp(b))
%
% Avoids flooring when a or b are very small
%
% author: Annie Liu
%

if a > b
    c = log(exp(b-a)+1) + a;
else
    c = log(exp(a-b)+1) + b;
end

return

