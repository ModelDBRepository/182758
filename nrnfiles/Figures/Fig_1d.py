#!/usr/bin/python
from neuron import h,gui
from matplotlib import pyplot

execfile('Cell.py')
execfile('STN.py')
execfile('simrun.py')
execfile('spikes.py')

stn = None
stn = STN()

tstop = 2000
stn.dur = 500

dif = 5
ilist = range(0,120,dif)
AHPlist = []

t_vec = h.Vector()
v_vec = h.Vector()
t_vec.record(h._ref_t)
v_vec.record(stn.soma(0.5)._ref_v)

for i in ilist:
	stn.amp = i
	stim = stn.attach_current_clamp()
	simulate(tstop)
	dur = AHP_dur(t_vec,v_vec,i,delay=stn.dur)
	AHPlist.append(dur)
#

fig, ax = pyplot.subplots(1,1)
duration = ax.plot(ilist, AHPlist, color='black',)

x = ax.set_xlabel('current (pA/um2)')
y = ax.set_ylabel('AHP Duration (s)')
#xt = ax.set_xlim([0,120])
#yt = ax.set_ylim([0.3,0.6])

fig.show()

