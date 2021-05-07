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

m2k_data = pd.read_csv(fpath+m2k_diff)
widths = np.arange(1, 31)
m2k_diff_cwt = cwt(m2k_data,ricker, widths)

plt.imshow(m2k_diff_cwt, extent=[-1, 1, 1, 31], cmap='PRGn', aspect='auto',
           vmax=abs(m2k_diff_cwt).max(), vmin=-abs(m2k_diff_cwt).max())
plt.show()

#plt.plot(m2k_data)
#plt.show()