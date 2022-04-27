# Copyright (C) 2022 Analog Devices, Inc.
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#     - Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     - Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in
#       the documentation and/or other materials provided with the
#       distribution.
#     - Neither the name of Analog Devices, Inc. nor the names of its
#       contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
#     - The use of this software may or may not infringe the patent rights
#       of one or more patent holders.  This license does not release you
#       from the requirement that you obtain separate licenses from these
#       patent holders to use this software.
#     - Use of the software either in source or binary form, must be run
#       on or directly connected to an Analog Devices Inc. component.
#
# THIS SOFTWARE IS PROVIDED BY ANALOG DEVICES "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, NON-INFRINGEMENT, MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED.
#
# IN NO EVENT SHALL ANALOG DEVICES BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, INTELLECTUAL PROPERTY
# RIGHTS, PROCUREMENT OF SUBSTIT11111111111111111111111111111111111111111111111111111111111111111111UTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
# THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
print("Program start")

from math import ceil 
from time import sleep as sec_delay
import matplotlib.pyplot as plt
import numpy as np
import os
import cn0501_aux_functions
print("Python Packages Import done")

from adi.ad7768 import ad7768
#import libm2k
#from py_utils.sin_params import *
from sin_params import *
print("ADI Packages Import done")

def write_csv(ch, power, ftype, sps):
    global srate
    cwd = os.getcwd()
    adc_properties = (str(power) + "_" + str(ftype) + "_" + str(srate[sps]['SPS']))
    fpath = cwd + "\examples\cn0501\csv_files\CH" + str(ch) + "\\"
    fname_dat = "DATA_" + adc_properties + ".csv"
    fname_param = "SINE_" + adc_properties + ".csv"

    try:
        with open(fpath+fname_dat, 'w+') as f:
            f.write("CH0,CH1,CH2,CH3,CH4,CH5,CH6,CH7" + '\n')
            print("Storing data to csv")
            for i in range(0, len(srate[sps]['DATA'][0]-1)):
                f.write(str(srate[sps]['DATA'][0][i]) + "," + str(srate[sps]['DATA'][1][i]) + "," +
                        str(srate[sps]['DATA'][2][i]) + "," + str(srate[sps]['DATA'][3][i]) + "," +
                        str(srate[sps]['DATA'][4][i]) + "," + str(srate[sps]['DATA'][5][i]) + "," +
                        str(srate[sps]['DATA'][6][i]) + "," + str(srate[sps]['DATA'][7][i]) + "," + '\n')
        print("---Data Log Done---\n\n")
        f.close()
        try:
            with open(fpath+fname_param, 'w') as f:
                f.write("SNR,THD,SINAD,ENOB,SFDR,FLOOR" + '\n')
                print("Storing sine param to csv")
                for i in range (0, len(srate[sps]['SNR']-1)):
                    f.write(str(srate[sps]['SNR'][i]) + "," + str(srate[sps]['THD'][i]) + "," +
                            str(srate[sps]['SINAD'][i]) + "," + str(srate[sps]['ENOB'][i]) + "," +
                            str(srate[sps]['SFDR'][i]) + "," + str(srate[sps]['FLOOR'][i]) + "," + '\n')
            print("---Sine Parameter Log Done---\n\n")
            f.close()
            
        except Exception as e_sine_log:
            print("\n Error Sine Param Log:")
            print(e_sine_log)

    except Exception as e_data_log:
        print("\n Error Data Log:")
        print(e_data_log)

class EndLoop( Exception ): pass

class ChErr( Exception ): pass

# This should eventually move into adi folder, and add an import to __init__
class cn0501(ad7768):
    def __init__(self, uri=""):
        ad7768.__init__(self, uri=uri)

    def single_capture(self):
        self.power_mode = "FAST_MODE" #FAST_MODE MEDIAN_MODE LOW_POWER_MODE
        self.filter = "WIDEBAND" #WIDEBAND SINC5
        self.sample_rate = 16000
        self.rx_buffer_size = self.sample_rate*2

        print("Sample Rate: ",self.sample_rate)
        print("Buffer Size: ",self.rx_buffer_size)
        print("Enabled Channels: ",self.rx_enabled_channels)
        x = self.rx()
        return x

    def run_sample_rate_tests(self, ch, power, ftype, sps):
        global srate
        if(True):
            print("Enabled Channels: ",self.rx_enabled_channels)
            print(self.power_mode_avail)
            self.power_mode = power
            print("Power Mode: ",self.power_mode)
            self.filter = ftype 
            print("Filter Type: ",self.filter)
            self.sample_rate = srate[sps]['SPS'] 
            print("Sample Rate: ",self.sample_rate)
            self.rx_buffer_size = int(self.sample_rate*2) #max 512000
            if self.rx_buffer_size > 512000:
                self.rx_buffer_size = 512000
            print("Buffer Size: ",self.rx_buffer_size)

            sec_rec = ceil(self.sample_rate/self.rx_buffer_size*nsecs/2) #use for n sec worth

            print("\nSwitching Sample Rate")
            sec_delay(2)

            print("\nSTART CAPTURE")
            for nloop in range(0,loops):
                sec_delay(1)
                print("." + str(nloop))

                vdata = np.empty(shape=(8,0)) # Change 8 to number of enabled channels
                for _ in range(int(sec_rec)):
                    vdata = np.concatenate((vdata, self.rx()), axis=1)
                
                #Capture data of last loop
                if (nloop == loops-1):
                    srate[sps]['DATA'] = vdata

                #Compute Sine parameters
                if(param_get == True):
                    #print("Calculating Sine Parameters")
                    harmonics, snr, thd, sinad, enob, sfdr, floor = sin_params(vdata[ch])
                    #srate[sps]['HARMONICS'] = np.concatenate((srate[sps]['HARMONICS'],[harmonics]),axis=0)
                    srate[sps]['SNR'] = np.concatenate((srate[sps]['SNR'],[snr]),axis=0)
                    srate[sps]['THD'] = np.concatenate((srate[sps]['THD'],[thd]),axis=0)
                    srate[sps]['SINAD'] = np.concatenate((srate[sps]['SINAD'],[sinad]),axis=0)
                    srate[sps]['ENOB'] = np.concatenate((srate[sps]['ENOB'],[enob]),axis=0)
                    srate[sps]['SFDR'] = np.concatenate((srate[sps]['SFDR'],[sfdr]),axis=0)
                    srate[sps]['FLOOR'] = np.concatenate((srate[sps]['FLOOR'],[floor]),axis=0)

                #Plot Data figures
                if (nloop == 0 and plot_show == True):
                    plt.figure(sps)
                    if(ch ==0 ):
                        plt.plot(vdata[0],color='red') #X GP
                    if(ch == 1):
                        plt.plot(vdata[1],color='blue') #Y GP
                    if(ch ==2):
                        plt.plot(vdata[2],color='green') #Z GP
            
            print("---Data Capture Done---\n\n")
        
        #Plot Average of Sine Params
        if(plot_show==True):
            snr_arr = []
            thd_arr =[]
            sinad_arr = []
            enob_arr = []
            sfdr_arr = []
            floor_arr = []
            sr = np.zeros(len(srate))
            for i in range(0,len(srate)):
                sr[i] = int(srate[i]['SPS'])
            for i in range(0,len(sr)):
                snr_arr = np.concatenate((snr_arr,[np.average(srate[i]['SNR'])]),axis=0)
                thd_arr = np.concatenate((thd_arr,[np.average(srate[i]['THD'])]),axis=0)
                sinad_arr = np.concatenate((sinad_arr,[np.average(srate[i]['SINAD'])]),axis=0)
                enob_arr = np.concatenate((enob_arr,[np.average(srate[i]['ENOB'])]),axis=0)
                sfdr_arr = np.concatenate((sfdr_arr,[np.average(srate[i]['SFDR'])]),axis=0)
                floor_arr = np.concatenate((floor_arr,[np.average(srate[i]['FLOOR'])]),axis=0)
            
            if (plot_show == True):
                plt.figure(101)
                plt.title("SNR")
                plt.plot(sr,snr_arr,marker="s")
                plt.figure(102)
                plt.title("THD")
                plt.plot(sr,thd_arr,marker="s")
                plt.figure(103)
                plt.title("SINAD")
                plt.plot(sr,sinad_arr,marker="s")
                plt.figure(104)
                plt.title("ENOB")
                plt.plot(sr,enob_arr,marker="s")
                plt.figure(105)
                plt.title("SFDR")
                plt.plot(sr,sfdr_arr,marker="s")
                plt.figure(106)
                plt.title("FLOOR")
                plt.plot(sr,floor_arr,marker="s")           

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#TEST PARAMETER VALUES
param_get = True
plot_show = False
loops = 10 #loops per channel 
nsecs = 4 #even number

#ADC TEST MODES
#power_modes = ['LOW_POWER_MODE', 'MEDIAN_MODE', 'FAST_MODE']
power_modes = ['FAST_MODE']
filter_types= ['WIDEBAND', 'SINC5']

#M2K TEST OUTPUTS
m2k_f = [10,100,1000,10000]
m2k_vp = [0.1,1,2.5,]
try:
    # Instantiate hardware
    mym2k = cn0501_aux_functions.wav_init()
    mycn0501 = cn0501(uri="ip:analog.local")
    #mycn0501 = cn0501(uri="ip:169.254.92.202")

    # Pick M2K output
    #cn0501_aux_functions.wavdiff_out(mym2k)
    #cn0501_aux_functions.seismic_out(mym2k)
    cn0501_aux_functions.sine_1k_out(mym2k,vp=1,f=4000) #max vp=2.5
    #cn0501_aux_functions.wavsingle_out(mym2k)

    while(True):
        srate = {0: {'SPS': 8000, 'DATA': [], 'HARMONICS': [],'SNR': [],'THD': [],'SINAD': [],'ENOB': [],'SFDR': [],'FLOOR': []},
                1: {'SPS': 16000, 'DATA': [], 'HARMONICS': [],'SNR': [],'THD': [],'SINAD': [],'ENOB': [],'SFDR': [],'FLOOR': []},
                2: {'SPS': 32000, 'DATA': [], 'HARMONICS': [],'SNR': [],'THD': [],'SINAD': [],'ENOB': [],'SFDR': [],'FLOOR': []},
                3: {'SPS': 64000, 'DATA': [], 'HARMONICS': [],'SNR': [],'THD': [],'SINAD': [],'ENOB': [],'SFDR': [],'FLOOR': []},
                4: {'SPS': 128000, 'DATA': [], 'HARMONICS': [],'SNR': [],'THD': [],'SINAD': [],'ENOB': [],'SFDR': [],'FLOOR': []},
                5: {'SPS': 256000, 'DATA': [], 'HARMONICS': [],'SNR': [],'THD': [],'SINAD': [],'ENOB': [],'SFDR': [],'FLOOR': []}}
        plt.clf()
        print("\n\nEnter GP CHANNEL, x:0 y:1 z:2 exit:-1")
        val = input()
        if (int(val) == -1):
            print("Ending loop...")
            raise EndLoop
        elif (int(val)>=0 and int(val)<=2):
            adc_ch = int(val)
            for p in power_modes:
                for f in filter_types:
                    for s in range(len(srate)-1,-1,-1):
                        mycn0501 = cn0501(uri="ip:analog.local")
                        if (p == 'MEDIAN_MODE'): #128kps max on Median mode
                            s = 4
                        elif (p == 'LOW_POWER_MODE'):  #32ksps max on Median mode
                            s = 2
                        mycn0501.run_sample_rate_tests(ch=adc_ch, power=p, ftype=f, sps= s)
                        write_csv(ch=adc_ch, power=p, ftype=f, sps= s)
                    del mycn0501
        else:
                raise ChErr

        if (plot_show == True):
            plt.show()
        
except EndLoop:
    print("Close M2K handler")
    cn0501_aux_functions.wav_close(mym2k)
    pass
except ChErr:
    print("\nEnter valid value")
except Exception as e:
    print("\n Error:")
    print(e)