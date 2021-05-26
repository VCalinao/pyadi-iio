import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd

import obspy
from obspy.imaging.cm import obspy_sequential
from obspy.signal.tf_misfit import cwt


#File directory of exported csv files  
print("File read")
cwd = os.getcwd()
fpath = cwd + "\examples\cn0501\csv_files\\"

m2k_out1 = "w1_ricker_wav_5vpp.csv"
m2k_out2 = "w2_ricker_wav_5vpp.csv"
m2k_diff = "diff_ricker_wav_5vpp.csv"

print("Data reshape")
m2k_data = np.asarray(pd.read_csv(fpath+m2k_diff))
m2k_data = np.reshape(m2k_data, [np.size(m2k_data)])

npts = np.size(m2k_data)
dt = 2/npts

t = np.linspace(0, dt * npts, npts)
f_min = 1
f_max = 1000

'''
'''

print("CWT")
scalogram = cwt(m2k_data, dt, 8, f_min, f_max)

print("Start plot")
fig = plt.figure(1)
ax = fig.add_subplot(211)

x, y = np.meshgrid(
    t,
    np.logspace(np.log10(f_min), np.log10(f_max), scalogram.shape[0]))

ax.pcolormesh(x, y, np.abs(scalogram), cmap=obspy_sequential)
ax.set_xlabel("Time [s]")
ax.set_ylabel("Frequency [Hz]")
ax.set_yscale('log')
ax.set_ylim(f_min, f_max)
'''
'''
m2k_o = fig.add_subplot(212)
m2k_o.plot(t,m2k_data)
m2k_o.set_xlabel("Time [s]")
m2k_o.set_ylabel("Amplitude [V]")
m2k_o.set_ylim(0, 5)

plt.show()