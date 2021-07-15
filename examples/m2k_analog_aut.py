# Copyright (c) 2019 Analog Devices Inc.
#
# This file is part of libm2k
# (see http://www.github.com/analogdevicesinc/libm2k).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 2.1 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

# This example assumes the following connections:
# W1 -> 1+
# W2 -> 2+
# GND -> 1-
# GND -> 2-
#
# The application will generate a sine and triangular wave on W1 and W2. The signal is fed back into the analog input
# and the voltage values are displayed on the screen

import libm2k
import matplotlib.pyplot as plt
import time
import numpy as np

ctx=libm2k.m2kOpen()
if ctx is None:
	print("Connection Error: No ADALM2000 device available/connected to your PC.")
	exit(1)

#ctx.calibrateADC()
ctx.calibrateDAC()

#ain=ctx.getAnalogIn()
aout=ctx.getAnalogOut()
#trig=ain.getTrigger()

#ain.enableChannel(0,True)
#ain.enableChannel(1,True)
#ain.setSampleRate(100000)
#ain.setRange(0,-10,10)

### uncomment the following block to enable triggering
#trig.setAnalogSource(0) # Channel 0 as source
#trig.setAnalogCondition(0,libm2k.RISING_EDGE_ANALOG)
#trig.setAnalogLevel(0,0.5)  # Set trigger level at 0.5
#trig.setAnalogDelay(0) # Trigger is centered
#trig.setAnalogMode(1, libm2k.ANALOG)


#Sine wave
#x = A*sin(2*np.pi*f*T+theta)+offset
#x=np.linspace(-np.pi,np.pi,1024)

#Frequency in Hertz
f = 10
#Samples per second
N = 750000
#Peak amplitude in Volts
vpeak = 1
#DC offset in volts
offset = vpeak

x=np.arange(0,1,1/N)

buffer2= vpeak*np.sin(2*np.pi*f*x) + offset

#Sawtooth
#buffer1=np.linspace(-2.0,2.00,1024)
#buffer1= [2]*len(buffer2)

buffer1 = buffer2

aout.setSampleRate(0, N)
aout.setSampleRate(1, N)
aout.enableChannel(0, True)
aout.enableChannel(1, True)

buffer = [buffer1, buffer2]

aout.setCyclic(True)
aout.push(buffer)

print("Enter to exit")
ex = input()

libm2k.contextClose(ctx)

