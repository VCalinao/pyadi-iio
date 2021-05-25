import math
import pandas as pd
import time
from scipy.signal import periodogram,find_peaks,ricker,cwt
import matplotlib.pyplot as plt
import numpy as np
import os

#File directory of exported csv files  
cwd = os.getcwd()
fpath = cwd + "\examples\cn0501\csv_files\\"


m2k_out1 = "w1_ricker_wav_5vpp.csv"
m2k_out2 = "w2_ricker_wav_5vpp.csv"
m2k_diff = "diff_ricker_wav_5vpp.csv"


m2k_data = np.asarray(pd.read_csv(fpath+m2k_diff))
m2k_data = np.reshape(m2k_data, [np.size(m2k_data)])

nw = int(np.size(m2k_data)/2/1000)

print(nw)
widths = np.arange(1,nw)
wavelet = ricker

m2k_diff_cwt = cwt(m2k_data,wavelet, widths)


plt.figure(1)
plt.imshow(m2k_diff_cwt, extent=[-10, 10, -100, 10000], cmap='PRGn', aspect='auto',
           vmax=abs(m2k_diff_cwt).max(), vmin=-abs(m2k_diff_cwt).max())

plt.figure(2)
plt.plot(m2k_data)
plt.show()
