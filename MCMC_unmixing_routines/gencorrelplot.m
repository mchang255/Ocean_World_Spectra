function gencorrelplot(MODS,bestmod,D)

set(0,'DefaultAxesFontSize',10)
set(0,'defaultfigurecolor',[1 1 1])

N = length(MODS(:,1));

dmin = D.prior_size_low;
dmax = D.prior_size_high;

theta_sort=sort(MODS,2,'ascend');
Nn = size(MODS,2);
confidence_percent1=68; % Percent confidence for credibility bounds
ithresh1=round((0.5*(100-confidence_percent1)/100)*Nn); % Note the factor of 1/2
ilo1=ithresh1; % This is the index of the lower bound
ihi1=Nn-ithresh1; % This is the index of the upper bound
lo1 = theta_sort(:,ilo1); % This is the lower bound
hi1 = theta_sort(:,ihi1); % This is the upper bound

confidence_percent2=95; % Percent confidence for credibility bounds
ithresh2=round((0.5*(100-confidence_percent2)/100)*Nn); % Note the factor of 1/2
ilo2=ithresh2; % This is the index of the lower bound
ihi2=Nn-ithresh2; % This is the index of the upper bound
lo2 = theta_sort(:,ilo2); % This is the lower bound
hi2 = theta_sort(:,ihi2); % This is the upper bound




figure('units','normalized','outerposition',[0 0 1 1])
for i = 1:N
    parami = MODS(i,:);
    for j = 1:N
        paramj = MODS(j,:);
        if i<=j
            subplot(N,N,N*(i-1)+j)
            if i==j
                if i<=N/2
                    hhh = histogram(parami,linspace(dmin(i),dmax(i),30));
                    hold on
                    plot([bestmod(i) bestmod(i)],[0 1.05.*max(hhh.Values)],'k')
                    plot([lo1(i) lo1(i)],[0 1.05.*max(hhh.Values)],'--k')
                    plot([hi1(i) hi1(i)],[0 1.05.*max(hhh.Values)],'--k')
                    plot([lo2(i) lo2(i)],[0 1.05.*max(hhh.Values)],':k')
                    plot([hi2(i) hi2(i)],[0 1.05.*max(hhh.Values)],':k')
                    xlabel(sprintf('Grain Size %i (micron)',i))
                    xlim([dmin(i) dmax(i)])
                    ylim([0 1.05.*max(hhh.Values)])
                else
                    hhh = histogram(parami,linspace(0,1,30));
                    hold on
                    plot([bestmod(i) bestmod(i)],[0 1.05.*max(hhh.Values)],'k')
                    plot([lo1(i) lo1(i)],[0 1.05.*max(hhh.Values)],'--k')
                    plot([hi1(i) hi1(i)],[0 1.05.*max(hhh.Values)],'--k')
                    plot([lo2(i) lo2(i)],[0 1.05.*max(hhh.Values)],':k')
                    plot([hi2(i) hi2(i)],[0 1.05.*max(hhh.Values)],':k')
                    xlabel(sprintf('Abundance %i (wt pct.)',i-N/2))
                    xlim([0 1])
                    ylim([0 1.05.*max(hhh.Values)])
                end
            else
                plot(paramj,parami,'+')
                if i<=N/2
                    ylim([dmin(i) dmax(i)])
                    if j<=N/2
                        xlim([dmin(j) dmax(j)])
                    else
                        xlim([0 1])
                    end
                else
                    ylim([0 1])
                    if j<=N/2
                        xlim([dmin(j) dmax(j)])
                    else
                        xlim([0 1])
                    end
                end
            end
            if j==N
                if i<=N/2
                    ylabel(sprintf('Grain Size %i (micron)',i))
                    set(gca,'yaxislocation','right');
                else
                    ylabel(sprintf('Abundance %i (wt pct.)',i-N/2))
                    set(gca,'yaxislocation','right');
                end
            end
        end
    end
end

breakpoint = 1;