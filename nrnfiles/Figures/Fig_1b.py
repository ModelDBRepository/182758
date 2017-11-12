#!/usr/bin/python
from neuron import h,gui
from matplotlib import pyplot

execfile('Cell.py')
execfile('STN.py')
execfile('simrun.py')

stn = None
stn = STN()

stn.soma.g0_Na = 0
tstop = 2000


dif = 5
ilist = range(-60,100+dif,dif)
vlist = []

for i in ilist:
	stn.amp = i
	stim = stn.attach_current_clamp()
	simulate(tstop)
	vlist.append(stn.soma.v)
#

fig, ax = pyplot.subplots(1,1)
mV = ax.plot(ilist, vlist, color='black',label='g_Na=0')
leg = ax.legend(loc='upper left')
x = ax.set_xlabel('current (pA/cm2)')
y = ax.set_ylabel('membrane Potential (mV)')
xt = ax.set_xlim([-60,100])
yt = ax.set_ylim([-120,-30])

fig.show()

