
import math
import pandas as pd
from scipy.signal import periodogram,find_peaks,ricker
import matplotlib.pyplot as plt
import numpy as np
import os
#print("Python Packages Import done")

from adi import ad7768
import libm2k
#print("ADI Packages Import done")

ctx=libm2k.m2kOpen()
if ctx is None:
    print("Connection Error: No ADALM2000 device available/connected to your PC.")
    exit(1)

#File directory of exported csv files  
cwd = os.getcwd()
fpath = cwd + "\examples\cn0501\csv_files\\"

ctx.calibrateDAC()
aout=ctx.getAnalogOut()  

#Samples per second
N = 750000
t = np.arange(0,1,1/N) 


#Ricker wavelet
vpp = 2                             #pk-pk amplitude of wavelet
n_peak= 2                           #Number of wavelet peaks
n_points = int(N/n_peak)            #number of points per wavelet
width_param = int(n_points*.05)     #5% width parameter
vcm = 2.5                           #VCM of AD7768 (2.5V default)

x = ricker(n_points,width_param)    #generate wavelet

v_scale = vpp/(np.max(x)-np.min(x))/2 #scale to fit vpp
x = x*v_scale

rick_offset = 0 - np.min(x)
x = x + rick_offset

if n_peak > 1:
    ricker_wav = np.concatenate((x,x))
    for _ in range(1,n_peak-1):
        ricker_wav= np.concatenate((ricker_wav,x))
else:
    ricker_wav = x

aout.setSampleRate(0, N)
aout.setSampleRate(1, N)
aout.enableChannel(0, True)
aout.enableChannel(1, True)


def wavsingle_out():
    w1_data = ricker_wav
    w2_data = ricker_wav

    buffer1 = w1_data
    buffer2 = w2_data
    buffer = [buffer1, buffer2]

    m2k_out = np.asarray(buffer1)
    m2k_out = m2k_out.reshape(N,1)

    DF = pd.DataFrame(m2k_out)

    f = "m2k_ricker_wav.csv"
    DF.to_csv(fpath+f, index = False, header = False)
   
    aout.setCyclic(True)
    aout.push(buffer)
    print("Wavelet Generated")

def wav_close():
    libm2k.contextClose(ctx)

def wavdiff_out():
    w1_data = ricker_wav +vcm
    w2_data = vcm-ricker_wav

    plt.plot(w1_data)
    plt.plot(w2_data)
    plt.plot(w1_data-w2_data)
    plt.show()

    buffer = [w1_data, w2_data]

    m2k_out1 = np.asarray(w1_data)
    m2k_out1 = m2k_out1.reshape(N,1)
    DF = pd.DataFrame(m2k_out1)

    m2k_out2 = np.asarray(w2_data)
    m2k_out2 = m2k_out2.reshape(N,1)
    DF = pd.DataFrame(m2k_out2)


    f1 = "w1_ricker_wav.csv"
    f2 = "w2_ricker_wav.csv"
    DF.to_csv(fpath+f1, index = False, header = False)
    DF.to_csv(fpath+f2, index = False, header = False)

    aout.setCyclic(True)
    aout.push(buffer)
    print("Wavelet Generated")

wavdiff_out()