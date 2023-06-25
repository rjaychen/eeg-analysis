% Modified to allow 16 channels by Ryan Chen, and save files under date
% name
% added sample duration feature. 

%% LOAD FILE
clear all;
close all;
clc;

%% LOAD FILES

% Prompt user for filename
[fname, fdir] = uigetfile( ...
{  '*.txt*',    'Text Files (*.txt*)'; ...
   '*.xlsx',    'Excel Files (*.xlsx)'; ...
   '*.csv*',    'Text Files (*.csv)'}, ...
   'Pick a file');

% Create fully-formed filename as a string
filename = fullfile(fdir, fname);
match = wildcardPattern + "\";
dataname = erase(filename, match); date = erase(dataname, 'OpenBCI-RAW-');
date = erase(date, '.txt');

% Check that file exists
assert(exist(filename, 'file') == 2, '%s does not exist.', filename);

% Read in the data, skipping the 5 first rows
data = readmatrix(filename);
    

%% GENERAL PARAMETERS

% Separate EEG data and auxiliary data
eegdata = data(:,2:17);          % EEG data (Columns 2:17)
auxdata = data(:,18:33);        % Aux data (Columns 18:33)

% General variables
time = (0:4:length(eegdata)*4-1)';  % Time vector
N_ch = 16;                           % Number of channels

% Band-pass Filtering Paramaters
% Referring to 
% FilterSettings.pde from OpenBCI_GUI repository on Github
fsamp = 125;                    % Sampling frequency --> for CyDai, 125 Hz
tsample = 1/fsamp;              % Period of samples
f_low = 60;                     % Cut frequency for low-pass filter
f_high = 1;                     % Cut frequency for high-pass filter

%% PRE-PROCESSING
% Bandpass Filter
for i=1:N_ch
    EEG(:,i)= bandpass_filter_8ch(eegdata(:,i), fsamp, f_low, f_high);
end

%crop data - change values below! 
 test_start = datetime(''); % first time stamp of data recorded
 sample_start = datetime(''); % desired trial start time
 sample_end = datetime(''); % desired trial end time
 eegdata1 = eegdata((seconds(sample_start - test_start)*fsamp+1):(seconds(sample_end-test_start)*fsamp),:); 
 EEG1 = EEG((seconds(sample_start - test_start)*fsamp+1):(seconds(sample_end-test_start)*fsamp),:); 
 
 % min 2 
 EEG2 = EEG((seconds(sample_end - test_start)*fsamp+1):((seconds(sample_end-test_start)+60)*fsamp),:); 

%% SAVE EEG DATA FOR EEGLAB
% Save raw data (unfiltered data)
save eegdata.txt eegdata1 -ascii;
save('eegdata.mat','eegdata1' );

% Save filtered data
save EEG.txt EEG -ascii; %maybe incorporate datetime info into naming of these files
savename = strcat('EEGf_', date, '.mat');
savename2 = strcat('EEGf_', date, '2.mat');
save(savename,'EEG1'); %changed to EEGf for convenience.
save(savename2,'EEG2');
