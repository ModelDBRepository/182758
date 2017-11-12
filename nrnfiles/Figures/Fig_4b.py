#!/usr/bin/python
#Figure 4b

from neuron import h,gui

execfile('Cell.py')
execfile('STN.py')
execfile('GPe.py')
execfile('simrun.py')
execfile('network.py')

tstop = 2000

# Control
amp=-.5
g2s=0#2.5
s2g=0.03
g2g=0.2

net = None
net = RSC(amp=amp,g2s=g2s,s2g=s2g,g2g=g2g)


cells = [net.stn_cells[0]]+[net.gpe_cells[0]]
cells[0].amp = -
cells[0].attach_current_clamp()

t_vec = h.Vector()
Ca_stn = h.Vector()
Ca_gpe = h.Vector()
t_vec.record(h._ref_t)
Ca_stn.record(cells[0].soma(0.5)._ref_Ca_AHP)
Ca_gpe.record(cells[1].soma(0.5)._ref_Ca_AHP)

simulate(tstop)

fig, ax = pyplot.subplots(2,1,sharex=True,sharey=False)
plot = ax[0].plot(t_vec, Ca_stn, color='black',label=cells[0].ident)
plot = ax[1].plot(t_vec, Ca_gpe, color='black',label=cells[1].ident)

x = pyplot.xlabel('time (s)')
y = pyplot.ylabel('[Ca++]')
#axis = pyplot.axis([0,2000,-100,50])
#tics = pyplot.yticks([-100,-50,0,50])

fig.show()

