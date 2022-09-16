% Example script to run CATMIP algorithm to sample a 2*Ncomponent-by-1 vector
% whose first Ncomponents elements are sizes, and second Ncomponent
% elements are corresponding abundances.
% Prior is uniform distribution on size, Dirichlet distribution on abundance.
% Data likelihood is multivariate normal (MVN) distribution
%
% Input parameters are highlighted with "***" in comments
%
%
% Please cite:
% Lapotre, M.G.A. et al. (2017), A probabilistic approach to remote
% compositional analysis of planetary surfaces, JGR: Planets, doi:
% 10.1002/2016JE005248

folder = what('mixtures');
files_list = dir(fullfile(folder.path, '*.txt'));

for z = 1:length(files_list)
    
    input_file = fullfile(folder.path, files_list(z).name);
    D=load_data(input_file); 
    
    % Matrix of samples of prior PDF.  Each column is one sample.
    THETA=zeros(D.Ncomponents,D.Nm); % Sizes
    for i=1:size(THETA,1)
        THETA(i,:)=unifrnd(D.prior_size_low(i),D.prior_size_high(i),1,D.Nm);
    end
    THETA = [THETA;                              % Sizes
             dirichletrnd_exc(D.prior_alpha,D.Nm)]; % Abundances
    
    
    % Function handle to evaluate prior PDF: accept model vector y and structure
    % return ln p(theta)
    llk_prior_handle = @llk_prior;
    
    % Function handle to evaluate data likelihood: accept model vector y,
    % structure, and ln p(theta), return ln p(D|theta) and (optionally) ln p(theta)
    for_model = @likelihood;
    
    % Setup complete
    
    %%%%%%%%%%%% Inversion %%%%%%%%%%%%%%%
    % Run CATMIP
    tic
    [THETA,LLK,nAccept,nReject]=...
        catmip_dirichlet(D.Nm,D.Nsteps,THETA,D,llk_prior_handle,for_model);
    toc
    
    % Return values:
    % THETA: Nparam x N x M+1 array.  M is total number of cooling steps.
    % THETA(:,:,1) are samples of the prior.  THETA(:,:,end) is final
    % solution. Each column of matrix at each cooling step is a single model.
    % LLK: 3 x N x M+1 array.  Same layout as THETA except each column of
    % matrix at each cooling step are the three log-likelihoods: 
    % ln [p(theta|D) p(D|theta) p(theta)]'
    % nAccept: M+1 x 1 array containing number of accepted sampls
    % nReject: M+1 x 1 array containing number of rejected sampls
    
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    lend = LLK(2,:,end);
    ind =  find(lend==max(lend));
    if length(ind)>1
        ind = ind(1);
    end
    MODS = THETA(:,:,end);
    bestmod = MODS(:,ind);
    MAP_grain_sizes_in_microns = bestmod(1:length(bestmod)/2) % This prints the MAP model (Ncomponent grain sizes in microns and Ncomponent mass abundances)
    MAP_abundances_in_percent = 100.*bestmod(length(bestmod)/2+1:end) 
    save('Results.mat','theta') % This saves the full results matrix to a ".mat" file
    
    abundances = what('abundances');
    filename_map = strcat(files_list(z).name, '_abundances.txt');
    file_map = fullfile(abundances.path, filename_map);
    writematrix(MAP_abundances_in_percent, file_map)

    
    genspectralplot(bestmod(length(bestmod)/2+1:length(bestmod)),bestmod(1:length(bestmod)/2),D.R_vs_SSA,input_file);
    residuals = what('residuals');
    filename = strcat(files_list(z).name,'_BestFit_and_Residual.jpg');
    saveas(gcf, fullfile(residuals.path, filename));
    % saveas(gcf,'BestFit_and_Residual.jpg')
    
    gencorrelplot(MODS,bestmod,D);
    distributions = what('distributions');
    filename_again = strcat(files_list(z).name,'_Distributions_and_Correlations.jpg');
    saveas(gcf, fullfile(distributions.path, filename_again));
    % saveas(gcf,'Distributions_and_Correlations.jpg')

end
