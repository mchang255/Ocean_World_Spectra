% source_dir = uigetdir(['mixtures']);
% disp(source_dir);
% d=dir([source_dir]);
% n=length(d);
% disp(n);

% folder = uigetdir('mixtures');
% files_list = dir(fullfile(folder, '*.txt'));
% disp(files_list)
% files_list(1).name

folder = what('mixtures');
files_list = dir(fullfile(folder.path, '*.txt'));
files_list(1).folder