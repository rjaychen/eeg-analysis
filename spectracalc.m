%% Band Power Calculation
srate = 125;
n_channels = 14;
clf;
sumD = 0; sumT = 0; sumA = 0; sumB = 0; sumG = 0;
for i=1:n_channels
    %figure(1);
    [spectra, freqs] = spectopo (EEG.data(i,:), EEG.pnts,...
        EEG.srate, 'percentage', 100, 'limits', [1 60 -20 35 nan nan]);
    
    deltaIdx = find(freqs>0.5 & freqs<4);
    thetaIdx = find(freqs>4 & freqs<8);
    alphaIdx = find(freqs>8 & freqs<13);
    betaIdx = find(freqs>13 & freqs<32);
    gammaIdx = find(freqs>32 & freqs<60);

    % compute absolute power
    % spectra output is in terms of 10*log(muV^2/Hz) -> convert to density
    % absolute band power is given by the integral of this curve,
    % density*freq-range.
    deltaPower = mean(10.^(spectra(deltaIdx)/10));
    thetaPower = mean(10.^(spectra(thetaIdx)/10));
    alphaPower = mean(10.^(spectra(alphaIdx)/10));
    betaPower = mean(10.^(spectra(betaIdx)/10));
    gammaPower = mean(10.^(spectra(gammaIdx)/10));
    sumD = sumD + deltaPower;
    sumT = sumT + thetaPower;
    sumA = sumA + alphaPower;
    sumB = sumB + betaPower;
    sumG = sumG + gammaPower;
end
%[spectra, freqs] = spectopo(EEG.data, EEG.pnts, EEG.srate, 'percentage', 100);

axis on; 
avgPowers = [sumD sumT sumA sumB sumG]/n_channels; % change number of channels here
disp(avgPowers)
disp("alpha/beta:" + avgPowers(3)/avgPowers(4))
disp("theta/beta:" + avgPowers(2)/avgPowers(4))