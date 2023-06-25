import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, lfilter_zi, iirnotch, freqz, filtfilt
import mne

#Band-filter methods
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a
    
def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    zi = lfilter_zi(b, a) * data[0]
    y, _ = lfilter(b, a, data, zi=zi)
    return y

#Band Decomposition
sampling_frequency = 125
filename = 'Subject_04_11_30\Subject_04_11_30\OpenBCISession_2022-11-30_15-34-09\BrainFlow-RAW_2022-11-30_15-34-09_0.csv'

df = pd.read_csv(filename, sep = '\t') #change file name
df.columns = ['Sample Index', 'EXG Channel 0', 'EXG Channel 1', 'EXG Channel 2', 'EXG Channel 3', 'EXG Channel 4', 'EXG Channel 5', 'EXG Channel 6', 'EXG Channel 7', 'EXG Channel 8', 'EXG Channel 9', 'EXG Channel 10', 'EXG Channel 11', 'EXG Channel 12', 'EXG Channel 13', 'EXG Channel 14', 'EXG Channel 15', 
'Accel Channel 0', 'Accel Channel 1', 'Accel Channel 2', 'Other', 'Other', 'Other', 'Other', 'Other', 'Other', 'Other', 'Analog Channel 0', 'Analog Channel 1', 'Analog Channel 2', 'Timestamp', 'Other']
channel1 = df[df.columns[1]] #desired channel, 1 = channel 1
channel2 = df[df.columns[2]]
channel3 = df[df.columns[3]]
channel4 = df[df.columns[4]]
channel5 = df[df.columns[5]]
channel6 = df[df.columns[6]]
channel7 = df[df.columns[7]]
channel8 = df[df.columns[8]]
channel9 = df[df.columns[9]]
channel10 = df[df.columns[10]]
channel11 = df[df.columns[11]]
channel12= df[df.columns[12]]
channel13 = df[df.columns[13]]
channel14 = df[df.columns[14]]
channel15 = df[df.columns[15]]
channel16 = df[df.columns[16]]

print(channel2)

################# mne interlude
# data= df.transpose().to_numpy()

# # assigning the channel type when initializing the Info object
# ch_names = ['Sample Index', 'EXG Channel 0', 'EXG Channel 1', 'EXG Channel 2', 'EXG Channel 3', 'EXG Channel 4', 'EXG Channel 5', 'EXG Channel 6', 'EXG Channel 7', 'EXG Channel 8', 'EXG Channel 9', 'EXG Channel 10', 'EXG Channel 11', 'EXG Channel 12', 'EXG Channel 13', 'EXG Channel 14', 'EXG Channel 15', 
# 'Accel Channel 0', 'Accel Channel 1', 'Accel Channel 2', 'Other', 'Other', 'Other', 'Other', 'Other', 'Other', 'Other', 'Analog Channel 0', 'Analog Channel 1', 'Analog Channel 2', 'Timestamp', 'Other']

# ch_types = ['misc', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 
#             'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 
#             'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'misc', 
#             'misc', 'misc', 'misc', 'misc', 'misc', 'misc', 'misc', 'misc', 'misc', 'misc', 'misc', 'misc', 'misc', 'misc']

# sampling_freq = 125  # in Hertz

# info = mne.create_info(ch_names= ch_names, ch_types = ch_types, sfreq= sampling_freq)

# User_raw = mne.io.RawArray(data, info)
# User_raw.set_eeg_reference(ref_channels = ['EXG Channel 6', 'EXG Channel 10'])
# print(User_raw.info)
# User_raw.plot_psd(fmax=40)
# User_raw.plot(duration = 595, n_channels = 16, block=True)
##################

# delta = butter_bandpass_filter(data = channel, lowcut = 0.1, highcut
#     = 4 , fs = sampling_frequency, order = 3)
# theta = butter_bandpass_filter(data = channel, lowcut = 4, highcut
#     = 8, fs = sampling_frequency, order = 3)
# alpha = butter_bandpass_filter(data = channel, lowcut = 8, highcut
#     = 13, fs = sampling_frequency, order = 3)
# beta = butter_bandpass_filter(data = channel, lowcut = 13, highcut
#     = 32, fs = sampling_frequency, order = 3)
# gamma = butter_bandpass_filter(data = channel, lowcut = 32, highcut
#     = 50, fs = sampling_frequency, order = 3)

#Visualization
fig = plt.figure(1)
plt.subplot(16,1,1)
plt.plot(channel1, linewidth=2)

plt.subplot(16,1,2)
plt.plot(channel2, linewidth=2)

plt.subplot(16,1,3)
plt.plot(channel3, linewidth=2)

plt.subplot(16,1,4)
plt.plot(channel4, linewidth=2)

plt.subplot(16,1,5)
plt.plot(channel5, linewidth=2)

plt.subplot(16,1,6)
plt.plot(channel6, linewidth=2)

plt.subplot(16,1,7)
plt.plot(channel7, linewidth=2)

plt.subplot(16,1,8)
plt.plot(channel8, linewidth=2)

plt.subplot(16,1,9)
plt.plot(channel9, linewidth=2)
# plt.subplot(6,1,2)
# plt.plot(delta, linewidth=2)

# plt.subplot(6,1,3)
# plt.plot(theta, linewidth=2)

# plt.subplot(6,1,4)
# plt.plot(alpha, linewidth=2)

# plt.subplot(6,1,5)
# plt.plot(beta, linewidth=2)

# plt.subplot(6,1,6)
# plt.plot(gamma, linewidth=2)

plt.show()

#FFT Denoising - Notch Filter
band_pass_eeg = butter_bandpass_filter(data = channel1, lowcut = 1,
                  highcut = 50, fs = 125, order = 3) #cyton eeg is 125Hz sampled
b_notch, a_notch = iirnotch(w0=59.9250936329588, Q=20, fs=250)
filtered_eeg = filtfilt(b_notch, a_notch, band_pass_eeg)

#Fourier Coefficients
number_of_points = len(filtered_eeg)
fhat = np.fft.fft(filtered_eeg, number_of_points)
PSD = fhat * np.conj(fhat) / number_of_points
freq = (1/(0.004*number_of_points))*np.arange(number_of_points)
L = np.arange(1,np.floor(number_of_points/2),dtype='int')

#Noise Filtration
indices = PSD > 150
PSDclean = PSD * indices
fhat = indices * fhat
ffilt = np.fft.ifft(fhat)

#Visualization
fig,axs = plt.subplots(3,1)
data_points = np.arange(number_of_points)
plt.sca(axs[0])
plt.plot(data_points,band_pass_eeg, color='k',linewidth=1.5,
               label='Bandpass filter')
plt.xlim(data_points[0],data_points[-1])
plt.legend()

plt.sca(axs[1])
plt.plot(data_points,ffilt,color='b',linewidth=2,
           label='FFT Filtered')
plt.xlim(data_points[0],data_points[-1])
plt.legend()

plt.sca(axs[2])
plt.plot(freq[L][3:75],PSD[L[3:75]],color= 'r',linewidth=2,
            label='Noisy')
plt.plot(freq[L][3:75],PSDclean[L][3:75],color='b',linewidth=1.5,
            label='Filtered')
plt.legend()
plt.xticks(freq[L][3:75:5])