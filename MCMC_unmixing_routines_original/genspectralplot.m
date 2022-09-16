function genspectralplot(ab,d,R_vs_SSA)
set(0,'defaultAxesFontSize', 18)
set(0,'defaultTextFontSize', 18)
set(0,'defaultfigurecolor',[1 1 1])

D = load_data;
ABm = ab;
Dm = d;

lt = D.lam_SPEC;
wt = D.R_SPEC;


Mm = gen_synthetic(ABm,Dm,R_vs_SSA);
lm = Mm(:,1);
wm = Mm(:,2);

wmi = interp1(lm,wm,lt);
yb = 1/length(wmi)*sum(wt);
inddd = find(~isnan(wmi));
wmi=wmi(inddd);
wt=wt(inddd);
lt=lt(inddd);
SStot = sum((wt-yb).^2);
SSres = sum((wt-wmi).^2);
R2 = 1-SSres/SStot;

figure
subplot(2,1,1)
plot(lt.*1e6,wt,'r','LineWidth',3)
hold on
plot(lm.*1e6,wm,'k','LineWidth',2)
legend('data',sprintf('model (R^2 = %.4f)',R2),'Location','NorthOutside')
xlabel('Wavelength, \lambda (\mum)')
if R_vs_SSA
    ylabel('Reflectance')
else
    ylabel('Single Scattering Albedo')
end
ylim([0 1])
xlim([min([min(lm.*1e6) min(lt.*1e6)]) max([max(lm.*1e6) max(lt.*1e6)])])
set(gcf,'color','w');
subplot(2,1,2)
plot(lt.*1e6,(wt./wmi-1).*100,'r','LineWidth',2)
hold on
plot(lt.*1e6,zeros(size(lt)),'k','LineWidth',1)
xlabel('Wavelength, \lambda (\mum)')
ylabel('Residual (%)')
xlim([min([min(lm.*1e6) min(lt.*1e6)]) max([max(lm.*1e6) max(lt.*1e6)])])
if abs(100.*(wt./wmi-1))<5
    ylim([-5 5])
end

hFig = gcf;
hFig.Units = 'inches';
set(hFig, 'Position', [1 1 5 8])


breakpoint = 1;