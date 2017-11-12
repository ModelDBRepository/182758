#!/usr/bin/python
from neuron import h,gui
from matplotlib import pyplot

execfile('Cell.py')
execfile('STN.py')
execfile('simrun.py')

stn = None
stn = STN()

dif = 5
scale = 10
vlist = [float(x)/dif for x in range(-90*dif,-20*dif+1)]
Ina = []
Ica = []
I_tot = []
I_g0 = []

for vstep in vlist:
	k = h.finitialize(vstep)
	Ina.append(stn.soma.I_Na*scale)
	Ica.append(stn.soma.I_Ca*scale)
	I = stn.soma.I_Ca+stn.soma.I_Na+stn.soma.I_K+stn.soma.I_AHP+stn.soma.I_Tstn+stn.soma.I_l
	I_tot.append(I*scale)


stn.soma.g0_Na = 0

for vstep in vlist:
	k = h.finitialize(vstep)
	I = stn.soma.I_K+stn.soma.I_Na+stn.soma.I_Ca+stn.soma.I_AHP+stn.soma.I_Tstn+stn.soma.I_l
	I_g0.append(I*scale)
#

fig, ax = pyplot.subplots(1,1)
ina = ax.plot(vlist, Ina, color='red',label='Na')
ica = ax.plot(vlist, Ica, color='green',label='Ca')
i_tot = ax.plot(vlist, I_tot, color='black',label='control')
i_g0 = ax.plot(vlist, I_g0, color='blue',label='g_Na=0')

leg = ax.legend(loc='upper left')
x = ax.set_xlabel('membrane Potential (mV)')
y = ax.set_ylabel('current (pA/um2)')
xt = ax.set_xlim([-90,-20])
yt = ax.set_ylim([-100,100])
tics = ax.set_yticks([-100,-60,-20,0,20,60,100])

fig.show()

