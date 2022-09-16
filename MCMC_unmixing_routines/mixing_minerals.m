P{1} = dlmread('gypsum.txt');
P{2} = dlmread('dolomite.txt');
P{3} = dlmread('calcite.txt');

l{1} = P{1}(:,1);
s{1} = P{1}(:,2);
t{1} = P{1}(:,3);
g1 = 242;
a1 = pi * (g1/2)^2;

l{2} = P{2}(:,1);
s{2} = P{2}(:,2);
t{2} = P{2}(:,3);
g2 = 285;
a2 = pi * (g2/2)^2;

l{3} = P{3}(:,1);
s{3} = P{3}(:,2);
t{3} = P{3}(:,3);
g3 = 410;
a3 = pi * (g3/2)^2;

a = [a1 a2 a3];
g = [g1 g2 g3];

[data, data2] = Hapke_opt_forward(a, g, s, t, l);

data = data.';

% data = [wavelength ssa];

T = table(data, data2);
writetable(T, 'mixed_spectra.txt');

% fileID = fopen('mixed_spectra.txt','w');
% fprintf(fileID,' %f %f\n', data, data2');
% fclose(fileID);
% for i = 1:2
    % fprintf(fileID,' %f %f\n',i, data');
% end
% fclose(fileID);