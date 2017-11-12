#!/usr/bin/python
from neuron import h,gui
from matplotlib import pyplot

execfile('Cell.py')
execfile('GPe.py')
execfile('simrun.py')

gpe = None
gpe = GPe()

gpe.soma.g0_Na = 0
tstop = 2000


dif = 3
ilist = [float(x)/dif for x in range(-10*dif,11*dif)]
vlist = []

for i in ilist:
	gpe.amp = i
	stim = gpe.attach_current_clamp()
	simulate(tstop)
	vlist.append(gpe.soma.v)
#

fig, ax = pyplot.subplots(1,1)
mV = ax.plot(ilist, vlist, color='black',label='g_Na=0')

leg = ax.legend(loc='upper left')
x = ax.set_xlabel('current (pA/cm2)')
y = ax.set_ylabel('membrane Potential (mV)')
xt = ax.set_xlim([-10,10])
yt = ax.set_ylim([-250,-50])
tics = ax.set_yticks([-250,-200,-150,-100,-50])

fig.show()

