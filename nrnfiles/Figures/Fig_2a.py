# Figure 2a
from neuron import h,gui

execfile('Cell.py')
execfile('GPe.py')
execfile('simrun.py')

gpe = None
gpe = GPe()

t_vec = h.Vector()
v_vec = h.Vector()
t_vec.record(h._ref_t)
v_vec.record(gpe.soma(0.5)._ref_v)

tstop = gpe.dur = 1000
ilist = [20,0,-0.25,140]

fig, ax = pyplot.subplots(len(ilist),1,sharex=False,sharey=False)

for i in range(len(ilist)-1):
	gpe.amp = ilist[i]
	cur = str(gpe.amp)
	label = 'Iapp=%s' % (cur)
	#
	stim = gpe.attach_current_clamp()
	simulate(tstop)
	ampname = 'amp = %snA' % (str(gpe.amp))
	plot = ax[i].plot(t_vec, v_vec, color='black',label=ampname)
	x = ax[i].set_xlim([0,1000])
	y = ax[i].set_ylim(-100,0,100)
	yt = ax[i].set_xticks(range(0,1200,200))
	xt = ax[i].set_yticks(range(-100,200,100))
	yl = ax[i].set_ylabel('voltage')
	leg = ax[].legend(fontsize = 'small', loc='top middle')
#

tstop = 350
gpe.amp=170
gpe.delay=100
gpe.dur=100
cur = str(gpe.amp)
label = 'Iapp=%s' % (cur)

stim = gpe.attach_current_clamp()
simulate(tstop)
ampname = 'amp = %snA' % (str(gpe.amp))
plot = ax[-1].plot(t_vec, v_vec, color='black',label=ampname)
x = ax[-1].set_xlim([0,350])
y = ax[-1].set_ylim([-85,-40])
yt = ax[-1].set_xticks(range(0,400,100))
xt = ax[-1].set_yticks(range(-80,-20,20))
xl = ax[-1].set_xlabel('time(s)')
yl = ax[-1].set_ylabel('voltage')
eg = ax[-1].legend(fontsize = 'small', loc='top middle')

pyplot.tight_layout()
pyplot.show()

