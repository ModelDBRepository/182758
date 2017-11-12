#!/usr/bin/python
from neuron import h,gui
from matplotlib import pyplot

execfile('Cell.py')
execfile('GPe.py')
execfile('simrun.py')
execfile('spikes.py')

gpe = None
gpe = GPe()

t_vec = h.Vector()
v_vec = h.Vector()
t_vec.record(h._ref_t)
v_vec.record(gpe.soma(0.5)._ref_v)

dif1 = 2
dif2 = 5
flist = []
ilist = range(0,20,2)+range(20,250,dif2)
tstop = 2000

for i in ilist:
	gpe.amp = i
	stim = gpe.attach_current_clamp()
	simulate(tstop)
	freq = detect_spikes(t_vec,v_vec)
	flist.append(freq)
	#
#

fig, ax = pyplot.subplots(1,1)
freq = ax.plot(ilist, flist, 'k-',label='control')

leg = ax.legend(loc='upper left')
x = ax.set_xlabel('current (pA/um2)')
y = ax.set_ylabel('frequency (spikes/sec)')
xt = ax.set_xlim([0,250])
yt = ax.set_ylim([0,500])

fig.show()

