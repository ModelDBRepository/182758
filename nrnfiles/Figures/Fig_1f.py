# Basic test

#!/usr/bin/python
from neuron import h,gui

execfile('Cell.py')
execfile('STN.py')
execfile('simrun.py')

stn = None
stn = STN()

t_vec = h.Vector()
v_vec = h.Vector()
t_vec.record(h._ref_t)
v_vec.record(stn.soma(0.5)._ref_v)

tstop = 2500
stn.delay = 650
stn.dur = 300
amplist = [-10,-20,-30]

fig, ax = pyplot.subplots(len(amplist),1,sharex=True,sharey=True)

for i in range(len(amplist)):
	stn.amp = amplist[i]
	stim = stn.attach_current_clamp()
	simulate(tstop)
	ampname = 'amp = %snA' % (str(stn.amp))
	plot = ax[i].plot(t_vec, v_vec, color='black',label=ampname)
	xt = ax[i].set_xlim([0,2500])
	yt = ax[i].set_ylim([-100,50])
	tics = ax[i].set_yticks([-100,-50,0,50])
	leg = ax[i].legend(fontsize = 'small', loc='upper left')
#

big_ax = fig.add_subplot(111)
big_ax.set_axis_bgcolor('none')
big_ax.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off')
x = big_ax.set_xlabel('time (ms)')
y = big_ax.set_ylabel('mV')

fig.show()

