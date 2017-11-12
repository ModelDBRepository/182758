#!/usr/bin/python
from neuron import h,gui
from matplotlib import pyplot

execfile('Cell.py')
execfile('STN.py')
execfile('simrun.py')
execfile('spikes.py')

flist = []
AHPlist = []
CaTlist = []
dif = 5
ilist = range(0,70+dif,dif)
tstop = 2000

for j in range(3):
	stn = None
	stn = STN()
	#
	t_vec = h.Vector()
	v_vec = h.Vector()
	t_vec.record(h._ref_t)
	v_vec.record(stn.soma(0.5)._ref_v)
	#
	if j==1:
		stn.soma.g0_Ca = stn.soma.g0_Tstn = 0
	#
	if j==2:
		stn.soma.g0_AHP = 0
	#
	for i in ilist:
		stn.amp = i
		stim = stn.attach_current_clamp()
		simulate(tstop)
		freq = detect_spikes(t_vec,v_vec)
		if j==0:
			flist.append(freq)
		#
		if j==1:
			CaTlist.append(freq)
		#
		if j==2:
			AHPlist.append(freq)
		#
	#
#

fig, ax = pyplot.subplots(1,1)

freq = ax.plot(ilist, flist, 'k-',label='control')
freq = ax.plot(ilist, CaTlist, 'k--',label='g_Ca=0, g_T=0')
freq = ax.plot(ilist, AHPlist, 'k:',label='gP_AHP=0')

leg = ax.legend(loc='upper left')
x = pyplot.xlabel('current (pA/um2)')
y = pyplot.ylabel('frequency (spikes/sec)')
#xt = ax.set_xlim([0,180])
#yt = ax.set_ylim([0,300])

fig.show()

